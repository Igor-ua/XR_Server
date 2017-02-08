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
import __builtin__
import requests
import sv_custom_utils
import time
import json

run_at_start = False
game_end_flag = False
ROOT_URL = 'http://127.0.0.1:8080'
players = list()


# Is called during every server frame
def check():
    try:
        # Run-once
        run_once()
        # If game state == 4 ('Game Ended') -> save stats.
        if server.GetGameInfo(GAME_STATE) == 4 and not game_end_flag:
            global game_end_flag
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


# Get Client's stats by UID
def get_client_stats(uid):
    try:
        url = ROOT_URL + '/stats/get/' + uid
        r = requests.get(url)
        r = json.loads(r.text)

        p = Player(r['uid'])
        p.last_used_name = r['lastUsedName']

        p.accuracy_stats.last_shots = r['accuracyStats']['lastShots']
        p.accuracy_stats.last_hits = r['accuracyStats']['lastHits']
        p.accuracy_stats.last_frags = r['accuracyStats']['lastFrags']
        p.accuracy_stats.accuracy_percent = r['accuracyStats']['lastAccuracyPercent']

        p.accuracy_stats.accumulated_shots = r['accuracyStats']['accumulatedShots']
        p.accuracy_stats.accumulated_hits = r['accuracyStats']['accumulatedHits']
        p.accuracy_stats.accumulated_frags = r['accuracyStats']['accumulatedFrags']
        p.accuracy_stats.accumulated_percent = r['accuracyStats']['accumulatedAccuracyPercent']

        p.awards.accumulated_mvp = r['awards']['accumulatedMvp']
        p.awards.accumulated_sadist = r['awards']['accumulatedSadist']
        p.awards.accumulated_survivor = r['awards']['accumulatedSurvivor']
        p.awards.accumulated_ripper = r['awards']['accumulatedRipper']
        p.awards.accumulated_phoe = r['awards']['accumulatedPhoe']
        p.awards.accumulated_aimbot = r['awards']['accumulatedAimbot']

        return p
    except:
        sv_custom_utils.simple_exception_info()


# Get Top stats by the info
# todo Not implemented yet
def get_top_stats(info):
    pass


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
    r = requests.put(url, data, headers=headers)
    print("[!]   Save stats result  ->  [%s, %s]" % (r.status_code, r.text))


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
    acs = AccuracyStats()
    try:
        [accuracyList_weapon, accuracyList_shots, accuracyList_kills, accuracyList_deaths,
         accuracyList_hits, accuracyList_siegehits, accuracyList_damage, accuracyList_last] = server.GetAccuracyList(
            guid)

        for weapon in range(0, accuracyList_last):
            if str(accuracyList_weapon[weapon]) == 'Coil Rifle':
                acs.uid = int(server.GetClientInfo(guid, INFO_UID))
                acs.shots = int(accuracyList_shots[weapon])
                acs.frags = int(accuracyList_kills[weapon])
                acs.hits = int(accuracyList_hits[weapon])
                acs.accuracy_percent = acs.hits * 100 / acs.shots
                acs.timestamp = int(round(time.time() * 1000))
    except:
        sv_custom_utils.simple_exception_info()
    return acs


# Gets accuracy for all active players
def calculate_players_with_accuracy():
    global players
    try:
        for index in xrange(0, sv_defs.objectList_Last):
            if sv_defs.objectList_Active[index]:
                uid = int(server.GetClientInfo(index, INFO_UID))
                if uid > 0:
                    player = Player(uid)
                    player.last_used_name = server.GetClientInfo(index, INFO_NAME)
                    player.kills = int(server.GetClientInfo(index, STAT_KILLS))
                    player.deaths = int(server.GetClientInfo(index, STAT_DEATHS))
                    player.killstreak = int(server.GetClientInfo(index, STAT_KILLSTREAK))
                    player.jumps = int(server.GetClientInfo(index, STAT_JUMPS))
                    player.npc_killed = int(server.GetClientInfo(index, STAT_NPCKILL))
                    player.mvp = player.kills - player.deaths
                    player.accuracy_stats = get_accuracy(index)
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
    # gs_transmit4 = map_awards.mvp
    core.CommandExec("set gs_transmit4 %s" % (map_awards.mvp["name"] + " - " + map_awards.mvp["value"]))
    # gs_transmit5 = map_awards.sadist
    core.CommandExec("set gs_transmit5 %s" % (map_awards.sadist["name"] + " - " + map_awards.sadist["value"]))
    # gs_transmit6 = map_awards.survivor
    core.CommandExec("set gs_transmit6 %s" % (map_awards.survivor["name"] + " - " + map_awards.survivor["value"]))
    # gs_transmit7 = map_awards.ripper
    core.CommandExec("set gs_transmit7 %s" % (map_awards.ripper["name"] + " - " + map_awards.ripper["value"]))
    # gs_transmit8 = map_awards.phoe
    core.CommandExec("set gs_transmit8 %s" % (map_awards.phoe["name"] + " - " + map_awards.phoe["value"]))
    # gs_transmit9 = map_awards.aimbot
    core.CommandExec("set gs_transmit9 %s" % (map_awards.aimbot["name"] + " - " + map_awards.aimbot["value"]))


# Don't save players with UID = 0 (0 is for unauthorized clients)
class Player(object):
    def __init__(self, uid):
        self.uid = uid
        self.last_used_name = ""
        self.accuracy_stats = AccuracyStats(self.uid)
        self.awards = Awards(self.uid)
        # These attributes should not be sent through the json
        self.kills = 0
        self.deaths = 0
        self.killstreak = 0
        self.npc_killed = 0
        self.mvp = 0
        pass

    def json_repr(self):
        return dict(uid=self.uid, lastUsedName=self.last_used_name, accuracyStats=self.accuracy_stats,
                    awards=self.awards)

    def __str__(self):
        return "Player: [UID: %s], [NAME: %s]" % (self.uid, self.last_used_name)


class AccuracyStats(object):
    def __init__(self, uid):
        self.uid = uid
        self.desc = 'Coil Rifle'

        self.last_shots = 0
        self.last_hits = 0
        self.last_frags = 0
        self.accuracy_percent = 0

        self.accumulated_shots = 0
        self.accumulated_hits = 0
        self.accumulated_frags = 0
        self.accumulated_percent = 0

        self.timestamp = 0

    def json_repr(self):
        return dict(uid=self.uid, desc=self.desc, lastShots=self.last_shots, lastFrags=self.last_frags,
                    lastHits=self.last_hits)

    def __str__(self):
        return "Coil Rifle: [UID: %s], [ACCURACY: %s], [SHOTS: %s], [FRAGS: %s], [HITS: %s]" % (
            self.uid, self.accuracy_percent, self.last_shots, self.last_frags, self.last_hits)


class MapAwards:
    def __init__(self):
        # most kills - deaths
        self.mvp = {"uid": 0, "name": "", "value": 0}
        # most kills
        self.sadist = {"uid": 0, "name": "", "value": 0}
        # most kills in a row
        self.survivor = {"uid": 0, "name": "", "value": 0}
        # most deaths
        self.ripper = {"uid": 0, "name": "", "value": 0}
        # most npcs killed
        self.phoe = {"uid": 0, "name": "", "value": 0}
        # most accurate
        self.aimbot = {"uid": 0, "name": "", "value": 0}


class Awards(object):
    def __init__(self, uid):
        self.uid = uid
        self.mvp = 0
        self.sadist = 0
        self.survivor = 0
        self.ripper = 0
        self.phoe = 0
        self.aimbot = 0

        self.accumulated_mvp = 0
        self.accumulated_sadist = 0
        self.accumulated_survivor = 0
        self.accumulated_ripper = 0
        self.accumulated_phoe = 0
        self.accumulated_aimbot = 0

    def json_repr(self):
        return dict(uid=self.uid, mvp=self.mvp, sadist=self.sadist, survivor=self.survivor,
                    ripper=self.ripper, phoe=self.phoe, aimbot=self.aimbot)

    def __str__(self):
        return "Awards : [UID: %s], [AIMBOT: %s], [MVP: %s], [SADIST: %s], [SURVIVOR: %s], [RIPPER: %s], [PHOE: %s]" \
               % (self.uid, self.aimbot, self.mvp, self.sadist, self.survivor, self.ripper, self.phoe)


__builtin__.DB_INFO_SHOTS = 1
__builtin__.DB_INFO_FRAGS = 2
__builtin__.DB_INFO_HITS = 3
__builtin__.DB_INFO_ACCURACY = 4
