# ---------------------------------------------------------------------------
#           Name: sv_instagib.py
#    Description: Instagib server trigger
# ---------------------------------------------------------------------------

# Savage API
import core
import server

# External modules
import sv_defs
import sv_utils
import random
import time
import threading
import sv_custom_utils

# Global vars
global game_mod
frag_limit = 0

are_flags_found = False
run_once_flag = True
end_run_once = True
type_list = ["CLIENT", "WORKER", "NPC", "MINE", "BASE", "OUTPOST", "BUILDING", "OTHER"]
teleport_locations = []
lock = threading.Lock()
dead_queue_lock = threading.Lock()

# A queue of dead players that should be revived
dead_queue = set()

INSTAGIB_MOD = "INSTAGIB"
available_game_states = (1, 2, 3)
reset_states = (1, 2)
need_reset = True

# human_stronghold was excluded from the teleport locations
possible_teleport_locations = ("spawnflag")

# Player's inventory structure
inventory = {}

# First-Last frags structure:
first_and_last_frag = {}
players_frags = {}

last_notify_time = 0
# Sec:
NOTIFY_PERIOD = 25 * 1000

# Is called during every server frame
def check():
    try:
        # Run-once
        run_once()

        # Reset vars
        global need_reset
        if server.GetGameInfo(GAME_STATE) in reset_states and need_reset:
            reset_clients_vars()
            need_reset = False

        # Runs only for INSTAGIB_MOD
        if game_mod != INSTAGIB_MOD:
            return 0

        # If game setup, warmup or normal
        if server.GetGameInfo(GAME_STATE) in available_game_states:
            iterate_through_clients()
            get_team_stats()
            update_clients_vars()
            is_time_to_finish()
        # Update latest stats for end-game status
        global end_run_once
        if server.GetGameInfo(GAME_STATE) == 4 and end_run_once:
            get_team_stats()
            update_clients_vars()
            end_run_once = False
    except:
        sv_custom_utils.simple_exception_info()
    return 0


def run_once():
    global run_once_flag
    if run_once_flag:
        run_once_flag = False
        core.ConsolePrint("________SV_INSTAGIB RUN-ONCE_______\n")
        check_mod()
        find_teleport_locations()
        get_vars_from_config()


# Checks the current mod of the game
def check_mod():
    global game_mod
    game_mod = core.CvarGetString('sv_map_gametype')
    core.ConsolePrint("[!]   MOD: %s\n" % game_mod)


def get_vars_from_config():
    global frag_limit
    frag_limit = int(core.CvarGetValue('py_instagib_fraglimit'))


# Gets an array of the team frags ([T1_FRAGS, T2_FRAGS]).
# There could be the same server variable and this duplicate logic is useless
def get_team_stats():
    objects_team_1 = []
    objects_team_2 = []
    global team_frags
    team_frags = [0, 0]
    for index in range(0, MAX_CLIENTS):
        if sv_defs.clientList_Team[index] == 1:
            objects_team_1.append(str(index))
        if sv_defs.clientList_Team[index] == 2:
            objects_team_2.append(str(index))
    for idx_1 in objects_team_1:
        frags = int(server.GetClientInfo(int(idx_1), STAT_KILLS))
        team_frags[0] += frags
        track_first_and_last_frag(idx_1, frags)
    for idx_2 in objects_team_2:
        frags = int(server.GetClientInfo(int(idx_2), STAT_KILLS))
        team_frags[1] += frags
        track_first_and_last_frag(idx_2, frags)
    return team_frags


def track_first_and_last_frag(guid, frags):
    global first_and_last_frag
    global players_frags
    # If game is in the normal state
    if server.GetGameInfo(GAME_STATE) == 3:
        if frags == 1 and 'first' not in first_and_last_frag:
            first_and_last_frag['first'] = guid
            core.CommandExec("set gs_first_frag_guid %s" % guid)
        if guid not in players_frags:
            players_frags[guid] = frags
        elif frags > players_frags[guid]:
            players_frags[guid] = frags
            first_and_last_frag['last'] = guid
            core.CommandExec("set gs_last_frag_guid %s" % guid)


# Global variables (gs_transmit1-3) that are being transferred to the clients:
def update_clients_vars():
    # gs_transmit1 = TEAM_1 Frags (RED)
    core.CommandExec("set gs_transmit1 %s" % team_frags[0])
    # gs_transmit2 = TEAM_2 Frags (BLUE)
    core.CommandExec("set gs_transmit2 %s" % team_frags[1])
    # gs_transmit3 = frag_limit
    core.CommandExec("set gs_transmit3 %s" % frag_limit)


def reset_clients_vars():
    for idx in range(1, 10):
        core.CommandExec("set gs_transmit%s 0" % idx)
    core.CommandExec("set gs_first_frag_guid -1")
    core.CommandExec("set gs_last_frag_guid -1")


def iterate_through_clients():
    for guid in xrange(0, sv_defs.objectList_Last):
        if sv_defs.objectList_Active[guid]:
            object_type = str(type_list[sv_defs.objectList_Type[guid]])
            object_health = int(sv_defs.objectList_Health[guid])
            if object_type == "CLIENT" and object_health == 0:
                teleport_and_revive(guid)
            if object_type == "CLIENT":
                check_for_frags_and_items(guid)
                # If game is in the 'setup' state - notify players to hit F3
                if server.GetGameInfo(GAME_STATE) == 1 or server.GetGameInfo(GAME_STATE) == 2:
                    notify_to_get_ready(guid)


def check_for_frags_and_items(guid):
    try:
        guid = int(guid)
        global inventory
        kills_for_mist = 5
        kills_for_sensor = 7
        kills_for_reloc = 10

        # Checking is there enough ammo in the Coil
        server.GameScript(guid, '!inventory target 1')
        slot1 = int(core.CvarGetString('gs_inventory_count'))
        if not bool(slot1):
            # !give target human_coilrifle ammo slot (slots: 0,1,2,3,4)
            server.GameScript(guid, '!give target human_coilrifle 100 1')

        server.GameScript(guid, '!inventory target 2')
        slot2 = bool(core.CvarGetString('gs_inventory_name'))
        server.GameScript(guid, '!inventory target 3')
        slot3 = bool(core.CvarGetString('gs_inventory_name'))
        server.GameScript(guid, '!inventory target 4')
        slot4 = bool(core.CvarGetString('gs_inventory_name'))
        kills = int(server.GetClientInfo(guid, STAT_KILLS))
        # killstreak = int(server.GetClientInfo(guid, STAT_KILLSTREAK))
        template = '^gReceived new item: ^y%s'
        if guid in inventory:
            if not bool(kills % kills_for_mist) and inventory[guid][0] != kills and not bool(slot2):
                server.GameScript(guid, '!give target beast_camouflage 1 2')
                inventory[guid][0] = kills
                server.Notify(guid, template % 'Mist Shroud')
            elif not bool(kills % kills_for_mist) and bool(slot2):
                inventory[guid][0] = kills
            if not bool(kills % kills_for_sensor) and inventory[guid][1] != kills and not bool(slot3):
                server.GameScript(guid, '!give target human_motion_sensor 1 3')
                inventory[guid][1] = kills
                server.Notify(guid, template % 'Sensor')
            elif not bool(kills % kills_for_sensor) and bool(slot3):
                inventory[guid][1] = kills
            if not bool(kills % kills_for_reloc) and inventory[guid][2] != kills and not bool(slot4):
                server.GameScript(guid, '!give target human_relocater 1 4')
                inventory[guid][2] = kills
                server.Notify(guid, template % 'Relocater')
            elif not bool(kills % kills_for_reloc) and bool(slot4):
                inventory[guid][2] = kills
        else:
            inventory[guid] = [0, 0, 0]
    except:
        sv_custom_utils.simple_exception_info()


def teleport_and_revive(guid):
    guid = int(guid)
    global dead_queue
    with dead_queue_lock:
        if guid not in dead_queue:
            dead_queue.add(guid)
            createThread('import sv_instagib; sv_instagib.execute_waiting_and_reviving(%s)' % guid)


def execute_waiting_and_reviving(guid):
    global dead_queue
    guid = int(guid)
    # Sleeping N seconds before any further actions. Is done to prevent interrupting of the death animation and effects
    time.sleep(1)

    # Check if client's hp > 0 - return (already teleported)
    if int(sv_defs.clientList_Health[guid]) > 0:
        dead_queue.remove(guid)
        return

    # If game state is setup, warmup or normal
    try:
        if server.GetGameInfo(GAME_STATE) in available_game_states:
            with lock:
                core.CommandExec('revive %s' % guid)
                Point3 = get_random_spawn_location()
                core.ConsolePrint("Teleporting: %s [%s, %s]\n" % (server.GetClientInfo(guid, INFO_NAME), Point3[0], Point3[1]))
                server.GameScript(guid, '!teleport target coords %s %s' % (Point3[0], Point3[1]))
                server.GameScript(guid, '!heal target 500')
                if guid in dead_queue:
                    dead_queue.remove(guid)
                time.sleep(0.5)
    except:
        sv_custom_utils.simple_exception_info()


# Finds all possible teleport location from the 'teleport_locations' list.
# Should be run-once at start
def find_teleport_locations():
    global are_flags_found
    global teleport_locations
    if not are_flags_found:
        for index in xrange(0, sv_defs.objectList_Last):
            if sv_defs.objectList_Active[index]:
                object_name = str(sv_defs.objectList_Name[index])
                if object_name in possible_teleport_locations:
                    teleport_locations.append(sv_utils.get_point3(index))
        core.ConsolePrint("Teleport locations[%s]:\n" % len(teleport_locations))
        for t in teleport_locations:
            core.ConsolePrint(" - %s\n" % t)
        are_flags_found = True


def get_random_spawn_location():
    return random.choice(teleport_locations)


# Checks conditions (such as time and frag limits) to end the current game
def is_time_to_finish():
    # Normal play mode: 3
    if server.GetGameInfo(GAME_STATE) == 3:
        # Dirty hack to count max_time without 1 second (was done to prevent overtime)
        max_time = int(core.CvarGetValue('gs_game_status_end')) - 1000
        current_time = int(core.CvarGetValue('gs_game_time'))
        team_frags = get_team_stats()
        if current_time >= max_time:
            core.CommandExec('endgame %s' % get_team_winner(team_frags))
            return
        if team_frags[0] == frag_limit and team_frags[1] == frag_limit:
            core.CommandExec('endgame 0')
            return
        if team_frags[0] == frag_limit:
            core.CommandExec('endgame 1')
            return
        if team_frags[1] == frag_limit:
            core.CommandExec('endgame 2')


def get_team_winner(team_frags):
    if team_frags[0] > team_frags[1]:
        return 1
    elif team_frags[0] < team_frags[1]:
        return 2
    return 0


def notify_to_get_ready(guid):
    global last_notify_time
    current_time_millis = int(round(time.time() * 1000))
    if current_time_millis > last_notify_time + NOTIFY_PERIOD:
        last_notify_time = current_time_millis
        server.Notify(guid, '^gGet ^gReady! ^yPress ^900F3 ^gto ^gstart ^gthe ^ggame.')


# Is called when check() returns 1
# Is not used in the current script
def execute():
    pass
