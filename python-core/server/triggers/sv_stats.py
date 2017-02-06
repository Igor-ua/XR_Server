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

run_once_flag = False


# Is called during every server frame
def check():
    try:
        # Run-once
        run_once()
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
        test_requests()


def test_requests():
    # core.ConsolePrint('[!]   db_stats\n')
    # url = 'http://localhost:8080/stats/all'
    # r = requests.get(url)
    # print r.text
    pass


# Get Client's stats by UID
def get_client_stats(index):
    try:
        pass
    except:
        sv_custom_utils.simple_exception_info()


# Get Top stats by the info
def get_top_stats(info):
    pass


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
    players = []
    try:
        for index in xrange(0, sv_defs.objectList_Last):
            if sv_defs.objectList_Active[index]:
                player = Player()
                player.uid = 0  # todo
                player.last_used_name = ""  # todo
                player.accuracy_stats = get_accuracy(int(index))
                # Avoid UID=0 from unauthorized clients
                if (player.accuracy_stats.uid > 0) and (player.accuracy_stats.last_shots > 0):
                    players.append(player)
    except:
        sv_custom_utils.simple_exception_info()
    return players


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
