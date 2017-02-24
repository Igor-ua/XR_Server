# ---------------------------------------------------------------------------
#           Name: sv_stats.py
#    Description: Server trigger that has to send/receive stats from the
#                 remote database via HTTP/JSON requests
# ---------------------------------------------------------------------------

# Savage API
import core
import server

# External modules
import sv_defs
import sv_utils
import requests
import sv_custom_utils
import time
import json
from sv_entities import *
import re


run_at_start = False
game_end_flag = False
ROOT_URL = 'http://127.0.0.1:8080'
players = list()
map_stats = MapStats()
# Cache for stats for one player during one round
single_stats_cache = {}
# Cache for top-stats during one round
top_stats_cache = {}
MAX_CACHE_SIZE = 30
# Will replace all symbols from the name that are not: '0-9A-Za-z-_() '
REGEXP_FOR_NAME = '[^0-9^A-Z^a-z^\-^_^(^) ]'


# Is called during every server frame
def check():
    try:
        # Run-once
        run_once()
        # If game state == 4 ('Game Ended') -> save stats.
        global game_end_flag
        if server.GetGameInfo(GAME_STATE) == 4 and not game_end_flag:
            game_end_flag = True
            calculate_players_and_awards()
            save_stats()
        return 0
    except:
        sv_custom_utils.simple_exception_info()


# Is called when check() returns 1
# Is not used in the current script
def execute():
    pass


def run_once():
    global run_at_start
    if not run_at_start:
        run_at_start = True
        print("________SV_STATS_______")
        global single_stats_cache
        single_stats_cache.clear()
        top_stats_cache.clear()


# Get Client's stats by UID
def get_client_stats(uid):
    try:
        global single_stats_cache
        if uid in single_stats_cache:
            return single_stats_cache[uid]
        else:
            url = ROOT_URL + '/stats/get/' + str(uid)
            resp = requests.get(url)
            resp = json.loads(resp.text)
            player = sv_custom_utils.get_player_from_json(resp)
            if len(single_stats_cache) > MAX_CACHE_SIZE:
                single_stats_cache.clear()
            single_stats_cache[uid] = player
            return player
    except:
        sv_custom_utils.simple_exception_info()


# Get Client's stats by last_used_name
def get_client_stats_by_name(name):
    try:
        url = ROOT_URL + '/stats/get/name/' + name
        resp = requests.get(url)
        resp = json.loads(resp.text)
        player = sv_custom_utils.get_player_from_json(resp)
        return player
    except:
        sv_custom_utils.simple_exception_info()


# Get Top Aimbots
def get_top_aimbots():
    try:
        cache_id = "aimbots"
        global top_stats_cache
        if cache_id in top_stats_cache:
            return top_stats_cache[cache_id]
        else:
            url = ROOT_URL + '/stats/get/top/aimbots'
            resp = requests.get(url)
            resp = json.loads(resp.text)
            aimbots = sv_custom_utils.get_list_of_players_from_json(resp)
            if len(top_stats_cache) > MAX_CACHE_SIZE:
                top_stats_cache.clear()
            top_stats_cache[cache_id] = aimbots
            return aimbots
    except:
        sv_custom_utils.simple_exception_info()


# Get Top Sadists
def get_top_sadists():
    try:
        cache_id = "sadists"
        global top_stats_cache
        if cache_id in top_stats_cache:
            return top_stats_cache[cache_id]
        else:
            url = ROOT_URL + '/stats/get/top/sadists'
            resp = requests.get(url)
            resp = json.loads(resp.text)
            sadists = sv_custom_utils.get_list_of_players_from_json(resp)
            if len(top_stats_cache) > MAX_CACHE_SIZE:
                top_stats_cache.clear()
            top_stats_cache[cache_id] = sadists
            return sadists
    except:
        sv_custom_utils.simple_exception_info()


# Get Top Survivors
def get_top_survivors():
    try:
        cache_id = "survivors"
        global top_stats_cache
        if cache_id in top_stats_cache:
            return top_stats_cache[cache_id]
        else:
            url = ROOT_URL + '/stats/get/top/survivors'
            resp = requests.get(url)
            resp = json.loads(resp.text)
            survivors = sv_custom_utils.get_list_of_players_from_json(resp)
            if len(top_stats_cache) > MAX_CACHE_SIZE:
                top_stats_cache.clear()
            top_stats_cache[cache_id] = survivors
            return survivors
    except:
        sv_custom_utils.simple_exception_info()


# Get Top Rippers
def get_top_rippers():
    try:
        cache_id = "rippers"
        global top_stats_cache
        if cache_id in top_stats_cache:
            return top_stats_cache[cache_id]
        else:
            url = ROOT_URL + '/stats/get/top/rippers'
            resp = requests.get(url)
            resp = json.loads(resp.text)
            rippers = sv_custom_utils.get_list_of_players_from_json(resp)
            if len(top_stats_cache) > MAX_CACHE_SIZE:
                top_stats_cache.clear()
            top_stats_cache[cache_id] = rippers
            return rippers
    except:
        sv_custom_utils.simple_exception_info()


# Get Top Phoes
def get_top_phoes():
    try:
        cache_id = "phoes"
        global top_stats_cache
        if cache_id in top_stats_cache:
            return top_stats_cache[cache_id]
        else:
            url = ROOT_URL + '/stats/get/top/phoes'
            resp = requests.get(url)
            resp = json.loads(resp.text)
            phoes = sv_custom_utils.get_list_of_players_from_json(resp)
            if len(top_stats_cache) > MAX_CACHE_SIZE:
                top_stats_cache.clear()
            top_stats_cache[cache_id] = phoes
            return phoes
    except:
        sv_custom_utils.simple_exception_info()


# Get Top MVPs
def get_top_mvps():
    try:
        cache_id = "mvps"
        global top_stats_cache
        if cache_id in top_stats_cache:
            return top_stats_cache[cache_id]
        else:
            url = ROOT_URL + '/stats/get/top/mvps'
            resp = requests.get(url)
            resp = json.loads(resp.text)
            mvps = sv_custom_utils.get_list_of_players_from_json(resp)
            if len(top_stats_cache) > MAX_CACHE_SIZE:
                top_stats_cache.clear()
            top_stats_cache[cache_id] = mvps
            return mvps
    except:
        sv_custom_utils.simple_exception_info()


# Get Top MVPs
def get_top_stats():
    get_top_aimbots()
    get_top_sadists()
    get_top_survivors()
    get_top_rippers()
    get_top_phoes()
    get_top_mvps()
    return top_stats_cache


def calculate_players_and_awards():
    global players
    calculate_players_with_accuracy()
    calculate_map_stats()
    map_awards = calculate_map_awards()
    bind_awards_to_players(map_awards)
    update_clients_vars(map_awards)


# Saves stats
def execute_save_stats():
    try:
        # Saves stats of players
        data = get_json_from_players()
        url = ROOT_URL + '/stats/server/players/put'
        headers = {'content-type': 'application/json'}
        resp = requests.put(url, data, headers=headers)
        print("[!]   Save players stats result  ->  [%s, %s]" % (resp.status_code, resp.text))
        # Saves map stats
        data = json.dumps(map_stats, default=sv_custom_utils.obj_repr)
        url = ROOT_URL + '/stats/server/map-stats/post'
        resp = requests.post(url, data, headers=headers)
        print("[!]   Save map stats result  ->  [%s, %s]" % (resp.status_code, resp.text))
    except:
        sv_custom_utils.simple_exception_info()


# Saves the stats of the players in the new thread
def save_stats():
    createThread('import sv_stats; sv_stats.execute_save_stats()')


# Gets the accuracy for the selected player by GUID
def get_accuracy(guid):
    guid = int(guid)
    # new object that will be returned
    acs = AccuracyStats(guid)
    try:
        [accuracyList_weapon, accuracyList_shots, accuracyList_kills, accuracyList_deaths,
         accuracyList_hits, accuracyList_siegehits, accuracyList_damage, accuracyList_last] = server.GetAccuracyList(
            guid)

        for weapon in range(0, accuracyList_last):
            if str(accuracyList_weapon[weapon]) == 'Coil Rifle':
                acs.uid = int(server.GetClientInfo(guid, INFO_UID))
                acs.last_shots = int(accuracyList_shots[weapon])
                acs.last_frags = int(accuracyList_kills[weapon])
                acs.last_hits = int(accuracyList_hits[weapon])
                if acs.last_shots == 0:
                    acs.accuracy_percent = 0
                else:
                    acs.accuracy_percent = acs.last_hits * 100 / acs.last_shots
                acs.timestamp = int(round(time.time() * 1000))
    except:
        sv_custom_utils.simple_exception_info()
    print acs
    return acs


# Gets accuracy for all active players
def calculate_players_with_accuracy():
    global players
    first_frag_guid = int(core.CvarGetValue('gs_first_frag_guid'))
    last_frag_guid = int(core.CvarGetValue('gs_last_frag_guid'))
    try:
        for guid in xrange(0, sv_defs.objectList_Last):
            if sv_defs.objectList_Active[guid]:
                uid = int(server.GetClientInfo(guid, INFO_UID))
                if uid > 0:
                    player = Player(uid)
                    clan_id = int(server.GetClientInfo(guid, INFO_CLANID))
                    player.clan_id = player.default_clan_id if clan_id == 0 else clan_id
                    player.last_used_name = re.sub(REGEXP_FOR_NAME, '', server.GetClientInfo(guid, INFO_NAME))
                    player.kills = int(server.GetClientInfo(guid, STAT_KILLS))
                    player.deaths = int(server.GetClientInfo(guid, STAT_DEATHS))
                    player.killstreak = int(server.GetClientInfo(guid, STAT_KILLSTREAK))
                    player.jumps = int(server.GetClientInfo(guid, STAT_JUMPS))
                    player.npc_killed = int(server.GetClientInfo(guid, STAT_NPCKILL))
                    player.mvp = player.kills - player.deaths
                    if player.kills > 0:
                        player.fpm = round(player.kills / (float(server.GetClientInfo(guid, STAT_ONTEAMTIME)) / 1000)
                                           * 60, 1)
                    if guid == first_frag_guid:
                        player.first_frag = 1
                    if guid == last_frag_guid:
                        player.last_frag = 1
                    player.accuracy_stats = get_accuracy(guid)
                    players.append(player)
    except:
        sv_custom_utils.simple_exception_info()


# Fill MapStats for save
def calculate_map_stats():
    global map_stats
    map_stats = MapStats()
    map_stats.map_name = 'set map name here'
    map_stats.red_score = int(core.CvarGetValue('gs_transmit1'))
    map_stats.blue_score = int(core.CvarGetValue('gs_transmit2'))
    if map_stats.red_score > map_stats.blue_score:
        map_stats.winner = 'red'
    elif map_stats.red_score < map_stats.blue_score:
        map_stats.winner = 'blue'


# Returns a JSON String of the list of players
# This string could be saved on the server
def get_json_from_players():
    return '{"Players": %s}' % json.dumps(players, default=sv_custom_utils.obj_repr)


# Calculates awards for active players
def calculate_map_awards():
    global players
    map_awards = MapAwards()
    frag_limit = int(core.CvarGetValue('sv_instagib_fraglimit'))
    red_score = int(core.CvarGetValue('gs_transmit1'))
    blue_score = int(core.CvarGetValue('gs_transmit2'))

    try:
        for p in players:
            # sadist
            if p.kills > map_awards.sadist["value"]:
                map_awards.sadist["uid"] = p.uid
                map_awards.sadist["clan_id"] = p.clan_id
                map_awards.sadist["name"] = p.last_used_name
                map_awards.sadist["value"] = p.kills
            # ripper
            if p.deaths > map_awards.ripper["value"]:
                map_awards.ripper["uid"] = p.uid
                map_awards.ripper["clan_id"] = p.clan_id
                map_awards.ripper["name"] = p.last_used_name
                map_awards.ripper["value"] = p.deaths
            # mvp
            if p.kills - p.deaths > map_awards.mvp["value"]:
                map_awards.mvp["uid"] = p.uid
                map_awards.mvp["clan_id"] = p.clan_id
                map_awards.mvp["name"] = p.last_used_name
                map_awards.mvp["value"] = p.kills - p.deaths
            # survivor
            if p.killstreak > map_awards.survivor["value"]:
                map_awards.survivor["uid"] = p.uid
                map_awards.survivor["clan_id"] = p.clan_id
                map_awards.survivor["name"] = p.last_used_name
                map_awards.survivor["value"] = p.killstreak
            # aimbot
            if p.accuracy_stats.accuracy_percent > map_awards.aimbot["value"]:
                map_awards.aimbot["uid"] = p.uid
                map_awards.aimbot["clan_id"] = p.clan_id
                map_awards.aimbot["name"] = p.last_used_name
                map_awards.aimbot["value"] = p.accuracy_stats.accuracy_percent
            # phoe
            if p.npc_killed > map_awards.phoe["value"]:
                map_awards.phoe["uid"] = p.uid
                map_awards.phoe["clan_id"] = p.clan_id
                map_awards.phoe["name"] = p.last_used_name
                map_awards.phoe["value"] = p.npc_killed
            # first frag
            if p.first_frag == 1:
                map_awards.first_frag["uid"] = p.uid
                map_awards.first_frag["clan_id"] = p.clan_id
                map_awards.first_frag["name"] = p.last_used_name
                map_awards.first_frag["value"] = p.first_frag
            # last frag that made your team win
            if p.last_frag == 1 and (red_score == frag_limit or blue_score == frag_limit):
                map_awards.last_frag["uid"] = p.uid
                map_awards.last_frag["clan_id"] = p.clan_id
                map_awards.last_frag["name"] = p.last_used_name
                map_awards.last_frag["value"] = p.last_frag
            # camper (0 deaths)
            if p.deaths == 0 and p.kills > 0:
                map_awards.camper["uid"] = p.uid
                map_awards.camper["clan_id"] = p.clan_id
                map_awards.camper["name"] = p.last_used_name
                map_awards.camper["value"] = p.deaths
            # fpm (frags per minute)
            if p.fpm > map_awards.fpm["value"]:
                map_awards.fpm["uid"] = p.uid
                map_awards.fpm["clan_id"] = p.clan_id
                map_awards.fpm["name"] = p.last_used_name
                map_awards.fpm["value"] = p.fpm
            # bunny
            if p.jumps > map_awards.bunny["value"]:
                map_awards.bunny["uid"] = p.uid
                map_awards.bunny["clan_id"] = p.clan_id
                map_awards.bunny["name"] = p.last_used_name
                map_awards.bunny["value"] = p.jumps

        # Retrieving info about clanAttr and merging it into the 'full_nick'
        uids = set()
        for attr, val in map_awards.__dict__.iteritems():
            if val["uid"] != 0:
                uids.add(val["uid"])
        info = sv_custom_utils.get_clients_info_dict(list(uids))
        for attr, val in map_awards.__dict__.iteritems():
            if val["uid"] != 0 and val["uid"] in info and info[val["uid"]]["ClanAbbrev"] != "":
                val["full_nick"] = '%s ^w^clan %s^ ^w%s' % (info[val["uid"]]["ClanAbbrev"], val["clan_id"], val["name"])
            elif val["uid"] != 0 and val["uid"] in info:
                val["full_nick"] = val["name"]
            else:
                val["full_nick"] = ""

    except:
        sv_custom_utils.simple_exception_info()
    return map_awards


# Binds awards to the owners
def bind_awards_to_players(map_awards):
    global players
    for p in players:
        p.awards.mvp = 1 if map_awards.mvp["uid"] == p.uid else 0
        p.awards.sadist = 1 if map_awards.sadist["uid"] == p.uid else 0
        p.awards.survivor = 1 if map_awards.survivor["uid"] == p.uid else 0
        p.awards.ripper = 1 if map_awards.ripper["uid"] == p.uid else 0
        p.awards.phoe = 1 if map_awards.phoe["uid"] == p.uid else 0
        p.awards.aimbot = 1 if map_awards.aimbot["uid"] == p.uid else 0


# Global variables (gs_transmit4-9) that are being transferred to the clients:
def update_clients_vars(map_awards):
    # gs_transmit4 = all awards in one variable with a ';' as a delimiter. Supposed to be parsed on the client side
    # like: python "import core; core.CvarSetString('val', core.CvarGetString('gs_transmit4').split(';')[0..etc])"
    core.CommandExec("set gs_transmit4 %s" % map_awards.get_transmit_value())

