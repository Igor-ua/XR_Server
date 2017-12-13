# ---------------------------------------------------------------------------
#           Name: sv_respawn_handler.py
#    Description: respawn handlers
# ---------------------------------------------------------------------------


# Savage API
import core
import server
import sv_defs


banned_clients = []
human_siege = ['human_ballista', 'human_catapult']
beast_siege = ['beast_summoner', 'beast_behemoth']
human_unit = 'human_nomad'
beast_unit = 'beast_scavenger'


def process_respawn(guid):
    core.ConsolePrint('Python: Player %s (%i) spawned as %s\n' % (server.GetClientInfo(guid, INFO_NAME), guid, sv_defs.objectList_Name[guid]))
    object_name = sv_defs.objectList_Name[guid]
    if is_camper_banned(guid):
        if object_name in human_siege:
            server.Notify(guid, 'Siege is banned for you! Pick up another unit.')
            server.GameScript(guid, '!changeunit target %s' % human_unit)
        if object_name in beast_siege:
            server.Notify(guid, 'Siege is banned for you! Pick up another unit.')
            server.GameScript(guid, '!changeunit target %s' % beast_unit)


def ban_siege_camper(guid):
    global banned_clients
    banned_clients.append(guid)


def unban_siege_campers():
    global banned_clients
    banned_clients = []


def is_camper_banned(guid):
    return guid in banned_clients
