# ---------------------------------------------------------------------------
#           Name: sv_respawn_handler.py
#    Description: respawn handlers
# ---------------------------------------------------------------------------


# Savage API
import core
import server
import sv_defs


banned_clients = []
human_siege = {'human_ballista': '4000', 'human_catapult': '7500'}
beast_siege = {'beast_summoner': '5500', 'beast_behemoth': '7500'}
human_unit = 'human_nomad'
beast_unit = 'beast_scavenger'


def process_respawn(guid):
    core.ConsolePrint('Python: Player %s (%i) spawned as %s\n' % (server.GetClientInfo(guid, INFO_NAME), guid, sv_defs.objectList_Name[guid]))
    if guid in banned_clients:
        warn_and_change_unit(guid)


def ban_siege_camper(guid):
    global banned_clients
    banned_clients.append(guid)
    server.Broadcast('^ySiege ^ywas ^900banned ^yfor ^g%s' % server.GetClientInfo(guid, INFO_NAME))
    warn_and_change_unit(guid)


def unban_siege_campers():
    global banned_clients
    banned_clients = []


def warn_and_change_unit(guid):
    object_name = sv_defs.objectList_Name[guid]
    object_team = str(sv_defs.objectList_Team[guid])
    if object_name in human_siege:
        server.Notify(guid, 'Siege is banned for you! Pick up another unit.')
        server.GameScript(guid, '!changeunit target %s' % human_unit)
        core.CommandExec('giveresource %s %s %s' % ('gold', human_siege[object_name], object_team))
    if object_name in beast_siege:
        server.Notify(guid, 'Siege is banned for you! Pick up another unit.')
        server.GameScript(guid, '!changeunit target %s' % beast_unit)
        core.CommandExec('giveresource %s %s %s' % ('gold', beast_siege[object_name], object_team))
