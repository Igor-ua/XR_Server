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
# Cache for stats for one player during one round
single_stats_cache = {}
# Cache for top-stats during one round
top_stats_cache = {}
MAX_CACHE_SIZE = 30
# Will replace all symbols from the name that are not: 'A-Za-z-_() '
REGEXP_FOR_NAME = '[^A-Z^a-z^\-^_^(^) ]'


# Is called during every server frame
def check():
    try:
        # Run-once
        run_once()
        # If game state == 4 ('Game Ended') -> save stats.
        global game_end_flag
        if server.GetGameInfo(GAME_STATE) == 4 and not game_end_flag:
            calculate_players_and_awards()
            save_stats()
            game_end_flag = True
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
    map_awards = calculate_map_awards()
    bind_awards_to_players(map_awards)
    update_clients_vars(map_awards)


# Saves the stats of the players
def execute_save_stats():
    global players
    data = get_json_from_players()
    url = ROOT_URL + '/stats/server/players/put'
    headers = {'content-type': 'application/json'}
    resp = requests.put(url, data, headers=headers)
    print("[!]   Save stats result  ->  [%s, %s]" % (resp.status_code, resp.text))


# Saves the stats of the players in the new thread
def save_stats():
    try:
        createThread('import sv_stats; sv_stats.execute_save_stats()')
    except:
        sv_custom_utils.simple_exception_info()


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
                acs.accuracy_percent = acs.last_hits * 100 / acs.last_shots
                acs.timestamp = int(round(time.time() * 1000))
    except:
        sv_custom_utils.simple_exception_info()
    print acs
    return acs


# Gets accuracy for all active players
def calculate_players_with_accuracy():
    global players
    try:
        for guid in xrange(0, sv_defs.objectList_Last):
            if sv_defs.objectList_Active[guid]:
                uid = int(server.GetClientInfo(guid, INFO_UID))
                if uid > 0:
                    player = Player(uid)
                    player.clan_id = int(server.GetClientInfo(guid, INFO_CLANID))
                    player.last_used_name = re.sub(REGEXP_FOR_NAME, '', server.GetClientInfo(guid, INFO_NAME))
                    player.kills = int(server.GetClientInfo(guid, STAT_KILLS))
                    player.deaths = int(server.GetClientInfo(guid, STAT_DEATHS))
                    player.killstreak = int(server.GetClientInfo(guid, STAT_KILLSTREAK))
                    player.jumps = int(server.GetClientInfo(guid, STAT_JUMPS))
                    player.npc_killed = int(server.GetClientInfo(guid, STAT_NPCKILL))
                    player.mvp = player.kills - player.deaths
                    player.accuracy_stats = get_accuracy(guid)
                    players.append(player)
    except:
        sv_custom_utils.simple_exception_info()


# Returns a JSON String of the list of players
# This string could be saved on the server
def get_json_from_players():
    return '{"Players": %s}' % json.dumps(players, default=sv_custom_utils.obj_repr)


# Calculates awards for active players
def calculate_map_awards():
    global players
    awards = MapAwards()
    try:
        for p in players:
            # sadist
            if p.kills > awards.sadist["value"]:
                awards.sadist["uid"] = p.uid
                awards.sadist["name"] = p.last_used_name
                awards.sadist["value"] = p.kills
            # ripper
            if p.deaths > awards.ripper["value"]:
                awards.ripper["uid"] = p.uid
                awards.ripper["name"] = p.last_used_name
                awards.ripper["value"] = p.deaths
            # mvp
            if p.kills - p.deaths > awards.mvp["value"]:
                awards.mvp["uid"] = p.uid
                awards.mvp["name"] = p.last_used_name
                awards.mvp["value"] = p.kills - p.deaths
            # survivor
            if p.killstreak > awards.survivor["value"]:
                awards.survivor["uid"] = p.uid
                awards.survivor["name"] = p.last_used_name
                awards.survivor["value"] = p.killstreak
            # aimbot
            if p.accuracy_stats.accuracy_percent > awards.aimbot["value"]:
                awards.aimbot["uid"] = p.uid
                awards.aimbot["name"] = p.last_used_name
                awards.aimbot["value"] = p.accuracy_stats.accuracy_percent
            # phoe
            if p.npc_killed > awards.phoe["value"]:
                awards.phoe["uid"] = p.uid
                awards.phoe["name"] = p.last_used_name
                awards.phoe["value"] = p.npc_killed
    except:
        sv_custom_utils.simple_exception_info()
    return awards


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

