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

run_once_flag = False
save_once_flag = False
ROOT_URL = 'http://127.0.0.1:8080'


# Is called during every server frame
def check():
    try:
        # Run-once
        run_once()
        # If game state == 4 ('Game Ended') -> save stats.
        if server.GetGameInfo(GAME_STATE) == 4:
            save_stats()
        return 0
    except:
        sv_custom_utils.simple_exception_info()


# Is called when check() returns 1
# Is not used in the current script
def execute():
    pass


def run_once():
    global run_once_flag
    if not run_once_flag:
        run_once_flag = True
        print("________SV_STATS_______")


# Get Client's stats by UID
# todo Not implemented yet
def get_client_stats(index):
    try:
        pass
    except:
        sv_custom_utils.simple_exception_info()


# Get Top stats by the info
# todo Not implemented yet
def get_top_stats(info):
    pass


# Saves the stats of the players
def execute_save_stats():
    players = get_players_with_accuracy()
    data = get_json_from_players(players)
    url = ROOT_URL + '/stats/server/players/put'
    headers = {'content-type': 'application/json'}
    r = requests.put(url, data, headers=headers)
    print("[!]   SAVE STATS: [%s, %s]" % (r.status_code, r.text))


# Saves the stats of the players in the new thread
def save_stats():
    try:
        if not save_once_flag:
            global save_once_flag
            createThread('import sv_stats; sv_stats.execute_save_stats()')
            save_once_flag = True
    except:
        sv_custom_utils.simple_exception_info()


# Gets the accuracy for the selected player by GUID
def get_accuracy(guid):
    guid = int(guid)
    # new object that will be returned
    coil_stats = AccuracyStats()
    try:
        [accuracyList_weapon, accuracyList_shots, accuracyList_kills, accuracyList_deaths,
         accuracyList_hits, accuracyList_siegehits, accuracyList_damage, accuracyList_last] = server.GetAccuracyList(
            guid)

        for weap in range(0, accuracyList_last):
            if str(accuracyList_weapon[weap]) == 'Coil Rifle':
                coil_stats.uid = int(server.GetClientInfo(guid, INFO_UID))
                coil_stats.shots = int(accuracyList_shots[weap])
                coil_stats.frags = int(accuracyList_kills[weap])
                coil_stats.hits = int(accuracyList_hits[weap])
                coil_stats.accuracy_percent = coil_stats.hits * 100 / coil_stats.shots
                coil_stats.timestamp = int(round(time.time() * 1000))
    except:
        sv_custom_utils.simple_exception_info()
    return coil_stats


# Gets accuracy for all active players
def get_players_with_accuracy():
    players = list()
    try:
        for index in xrange(0, sv_defs.objectList_Last):
            if sv_defs.objectList_Active[index]:
                player = Player()
                player.uid = int(server.GetClientInfo(index, INFO_UID))
                player.last_used_name = server.GetClientInfo(index, INFO_NAME)
                player.accuracy_stats = get_accuracy(index)
                if (player.accuracy_stats.uid > 0) and (player.accuracy_stats.last_shots > 0):
                    players.append(player)
    except:
        sv_custom_utils.simple_exception_info()
    return players


# Returns a JSON String of the list of players
# This string could be saved on the server
def get_json_from_players(players):
    return '{"Players": %s}' % json.dumps(players, default=sv_custom_utils.obj_repr)


# Don't save players with UID = 0 (0 is for unauthorized clients)
class Player:
    def __init__(self):
        self.uid = 0
        self.last_used_name = ""
        self.accuracy_stats = AccuracyStats()
        pass

    def json_repr(self):
        return dict(uid=self.uid, lastUsedName=self.last_used_name, accuracyStats=self.accuracy_stats)

    def __str__(self):
        return "Player: [UID: %s], [NAME: %s]" % (self.uid, self.last_used_name)


class AccuracyStats:
    def __init__(self):
        self.uid = 0
        self.desc = 'Coil Rifle'
        self.last_shots = 0
        self.last_hits = 0
        self.last_frags = 0
        self.accuracy_percent = 0
        self.timestamp = 0

    def json_repr(self):
        return dict(uid=self.uid, desc=self.desc, lastShots=self.last_shots, lastFrags=self.last_frags,
                    lastHits=self.last_hits)

    def __str__(self):
        return "Coil Rifle: [UID: %s], [ACCURACY: %s], [SHOTS: %s], [FRAGS: %s], [HITS: %s]" % (
            self.uid, self.accuracy_percent, self.last_shots, self.last_frags, self.last_hits)


__builtin__.DB_INFO_SHOTS = 1
__builtin__.DB_INFO_FRAGS = 2
__builtin__.DB_INFO_HITS = 3
__builtin__.DB_INFO_ACCURACY = 4
