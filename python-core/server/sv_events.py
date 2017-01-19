# ---------------------------------------------------------------------------
#           Name: sv_events.py
#         Author: Anthony Beaucamp (aka Mohican)
#    Description: Silverback Event Entries (init, frame, status changes)
#          State: modified
# ---------------------------------------------------------------------------

# Savage API
import core
import server

# External modules
import sv_defs
import sv_maps
import sv_triggers
import sv_custom_utils


# -------------------------------
# Called directly by Silverback
# -------------------------------
def init():
    # Print Console Message
    core.ConsolePrint('Sv_Events: Initializing Server-Side...\n')

    try:
        # Init Server Modules
        sv_maps.init()
        sv_triggers.init()

        global sv_message_processor
        import sv_message_processor
        sv_message_processor.init()

    except:
        sv_custom_utils.simple_exception_info()


# -------------------------------
# Called directly by Silverback
# -------------------------------
def frame():
    try:
        # Refresh System Information
        sv_defs.gameTime = server.GetGameInfo(GAME_TIME)

        # Refresh Object Data
        [sv_defs.objectList_Active, sv_defs.objectList_Team, sv_defs.objectList_Type,
         sv_defs.objectList_Name, sv_defs.objectList_Health, sv_defs.objectList_MaxHealth,
         sv_defs.objectList_Construct, sv_defs.objectList_Last] = server.GetObjectList()

        # Refresh Client Data
        [sv_defs.clientList_Active, sv_defs.clientList_Bot, sv_defs.clientList_Team,
         sv_defs.clientList_Officer, sv_defs.clientList_Squad, sv_defs.clientList_Charge,
         sv_defs.clientList_Mana, sv_defs.clientList_MaxMana, sv_defs.clientList_Health,
         sv_defs.clientList_MaxHealth, sv_defs.clientList_Stamina,
         sv_defs.clientList_MaxStamina] = server.GetClientList()

        # Refresh Team Data
        [sv_defs.teamList_Base, sv_defs.teamList_Commander, sv_defs.teamList_RaceName,
         sv_defs.teamList_RaceDesc, sv_defs.teamList_Missions, sv_defs.teamList_Last] = server.GetTeamList()

        # Check Triggers
        sv_triggers.frame()

        # Refresh Statistics (sv_newerth.py)
        Server_StatsFrame()

    except:
        pass


# -------------------------------
# Called directly by Silverback
# -------------------------------
def status():
    try:
        # Get the new Game State
        state = server.GetGameInfo(GAME_STATE)

        if state == 0:
            # Server is waiting for clients to connect
            core.ConsolePrint('> Game state: [Server is Empty]\n')

        elif state == 1:
            # Setting a game up in the lobby
            core.ConsolePrint('> Game state: [Game Setup]\n')

        elif state == 2:
            # Warming up
            core.ConsolePrint('> Game state: [Game Warmup]\n')

        elif state == 3:
            # Normal play mode
            core.ConsolePrint('> Game state: [Game Normal]\n')

        elif state == 4:
            # Game has ended
            core.ConsolePrint('> Game state: [Game Ended]\n')

        elif state == 5:
            # About to load the next map
            core.ConsolePrint('> Game state: [Loading Next Map]\n')
            sv_maps.savestats()
            sv_maps.nextmap()

        elif state == 6:
            # About to load the voted map
            core.ConsolePrint('> Game state: [Loading Voted Map]\n')
            sv_maps.savestats()

        elif state == 7:
            # Match is restarting (same map)
            core.ConsolePrint('> Game state: [Restarting Map]\n')
            sv_maps.savestats()

        # Reload Trigger (resets trigger states)
        sv_triggers.re_load()

        # Reset Statistics (sv_newerth.py)
        Server_StatsReset()

    except:
        pass


# -------------------------------
# Called directly by Silverback
# -------------------------------
def callvote(guid, vote_type, vote_info):
    # Accept vote by default
    answer = 1
    try:
        # Calling Map Vote?
        if vote_type == 'world':
            answer = sv_maps.callvote(guid, vote_info)
    except:
        sv_custom_utils.simple_exception_info()

    return answer


# message_type strings: global, team, squad, selected
def chatmessage(guid, message_type, message):
    # Accept chat by default
    answer = 1
    try:
        answer = sv_message_processor.process_chat_message(guid, message_type, message)
    except:
        sv_custom_utils.simple_exception_info()
    return answer


def privatemessage(sender_idx, receiver_idx, message):
    # Accept private message by default
    answer = 1
    try:
        answer = sv_message_processor.process_private_message(sender_idx, receiver_idx, message)
    except:
        sv_custom_utils.simple_exception_info()
    return answer


def clientconnect(guid):
    core.ConsolePrint('   -> Connected GUID: %i\n' % guid)


def clientdisconnect(guid):
    core.ConsolePrint('   <- Disconnected GUID: %i\n' % guid)


