# ---------------------------------------------------------------------------
#           Name: sv_defs.py
#         Author: Anthony Beaucamp (aka Mohican)
#  Last Modified: 11/12/2010
#    Description: Server-side Global Definitions
# ---------------------------------------------------------------------------

import __builtin__

# System Information
global gameTime

# Object Data Lists (see server.GetObjectList())
global objectList_Active    # Is Object active?
global objectList_Team      # Which Team does the Object belong to?
global objectList_Type      # What Type of Object? (see OBJTYPE_***)
global objectList_Name      # Name of Object (ex: 'human_nomad')
global objectList_Health    # Object's Health Point
global objectList_MaxHealth # Object's Max Health Point
global objectList_Construct # Is Object under construction? (only applies to Buildings)
global objectList_Last      # Index of last Object

# Client Data Lists (also correspond to index 0-127 of object list above, see server.GetClientList())
global clientList_Active     # Is Client Active? (Different than objectList_Active above)
global clientList_Bot        # Is Client a Bot?
global clientList_Team       # Client's Team
global clientList_Officer    # Is Client an Officer?
global clientList_Squad      # Squad that Client belongs to
global clientList_Charge     # Client's Weapon Charge Status (%)
global clientList_Mana       # Client's Mana Points
global clientList_MaxMana    # Client's Max Mana Points
global clientList_Health     # Client's Health Points
global clientList_MaxHealth  # Client's Max Health Points
global clientList_Stamina    # Client's Stamina Points
global clientList_MaxStamina # Client's Max Stamina Points

# Team Data Lists (see server.GetTeamList())
global teamList_Base      # Index of Team's Base (Stronghold/Lair)
global teamList_Commander # Index of Team's Commander
global teamList_RaceName  # Team's Race Name (ex: human)
global teamList_RaceDesc  # Team's Race Description (ex: The Beast Horde)
global teamList_Missions  # Squad Missions of each Team
global teamList_Last      # Index of last Team

# Game Information Types (see server.GetGameInfo())
__builtin__.GAME_TIME = 0       # Game Time (in msec)
__builtin__.GAME_STATE = 1      # Game State (see sv_events.py)
__builtin__.GAME_WINTEAM = 2    # Last Winner Team

# Client Information Types (see server.GetClientInfo())
__builtin__.INFO_ACTIVE	= 0       # Is Client active?
__builtin__.INFO_TEAM = 1         # Client's Team
__builtin__.INFO_NAME = 2         # Client's Name
__builtin__.INFO_UID = 3          # Client's UID
__builtin__.INFO_GUID = 4         # Client's GUID
__builtin__.INFO_CLANID = 5       # Client's CLANID
__builtin__.INFO_STATUS = 6       # Client's status
__builtin__.INFO_TYPING	= 7       # Is Client typing?
__builtin__.INFO_REFEREE = 8      # Is Client referee?
__builtin__.STAT_DEATHS = 9       # Client's deaths
__builtin__.STAT_KILLS = 10       # Client's kills
__builtin__.STAT_KILLSTREAK = 11  # Client's kill steak
__builtin__.STAT_BLOCKS = 12      # Client's succesfull blocks
__builtin__.STAT_JUMPS = 13       # Client's jumps
__builtin__.STAT_CARNHP = 14      # Client's HP earned with Carn
__builtin__.STAT_NPCDMG = 15      # Client's NPC damage
__builtin__.STAT_NPCKILL = 16     # Client's NPC kills
__builtin__.STAT_PEONDMG = 17     # Client's Peon damage
__builtin__.STAT_PEONKILL = 18    # Client's Peon kills
__builtin__.STAT_BUILDDMG = 19    # Client's Building damage
__builtin__.STAT_BUILDKILL = 20   # Client's Building kills
__builtin__.STAT_OUTPOSTDMG = 21  # Client's Outpost damage
__builtin__.STAT_CLIENTDMG = 22   # Damage caused to other Clients
__builtin__.STAT_MELEEKILL = 23   # Melee kills
__builtin__.STAT_RANGEDKILL = 24  # Ranged kills
__builtin__.STAT_SIEGEKILL = 25   # Siege Units killed by Client
__builtin__.STAT_MINE = 26        # Mining XP
__builtin__.STAT_HEAL = 27        # Healing XP
__builtin__.STAT_BUILD = 28       # Building XP
__builtin__.STAT_MONEYGAIN = 29   # Money earned
__builtin__.STAT_MONEYSPEND = 30  # Money spent
__builtin__.STAT_ORDERGIVE = 31   # Orders given by Client
__builtin__.STAT_ORDEROBEY = 32   # Orders obeyed by Client
__builtin__.STAT_EXPERIENCE = 33  # Total XP gained by Client
__builtin__.STAT_AUTOBUFF = 34    # Auto-buffs used by Client
__builtin__.STAT_SACRIFICE = 35   # Sacrifices used by Client
__builtin__.STAT_FLAGCAPTURE = 36 # Flags captured by Client
__builtin__.STAT_CONNECTTIME = 37 # Time connected to server
__builtin__.STAT_ONTEAMTIME = 38  # Time spent playing
__builtin__.INFO_CANCOMMTIME = 39 # Time after the Client can command again
__builtin__.INFO_REFSTATUS = 40   # 'none', 'guest', 'normal' or 'god'

# Max Definitions
__builtin__.MAX_OBJECTS = 1024
__builtin__.MAX_CLIENTS = 128
__builtin__.MAX_SQUADS = 7
__builtin__.MAX_TEAMS = 9
__builtin__.MAX_BACKUPS = 127

# Object Types
__builtin__.OBJTYPE_CLIENT = 0
__builtin__.OBJTYPE_WORKER = 1
__builtin__.OBJTYPE_NPC = 2
__builtin__.OBJTYPE_MINE = 3
__builtin__.OBJTYPE_BASE = 4
__builtin__.OBJTYPE_OUTPOST = 5
__builtin__.OBJTYPE_BUILDING = 6
__builtin__.OBJTYPE_OTHER = 7

# Mine Types
__builtin__.MINETYPE_ANY = 0
__builtin__.MINETYPE_GOLD = 1
__builtin__.MINETYPE_STONE = 2

# Inventory Types
__builtin__.INVTYPE_NONE = 0
__builtin__.INVTYPE_MELEE = 1
__builtin__.INVTYPE_RANGED = 2
__builtin__.INVTYPE_ITEM = 3

# Input Angle IDs
__builtin__.ANGLE_PITCH = 0
__builtin__.ANGLE_YAW = 1
__builtin__.ANGLE_ROLL = 2

# Input Motion IDs
__builtin__.MOVE_FORWARD = 0
__builtin__.MOVE_BACKWARD = 1
__builtin__.MOVE_LEFT = 2
__builtin__.MOVE_RIGHT = 3
__builtin__.MOVE_JUMP = 4
__builtin__.MOVE_CROUCH = 5
__builtin__.MOVE_STOP = 6

# Input Button IDs
__builtin__.BUTTON_ATTACK = 0
__builtin__.BUTTON_BLOCK = 1
__builtin__.BUTTON_USE = 2
__builtin__.BUTTON_SPRINT = 3
__builtin__.BUTTON_CHARGE = 4
__builtin__.BUTTON_WORK = 5

# Navigation Order IDs (GOAL: obj->goal)
__builtin__.ORDER_NONE = 0
__builtin__.ORDER_MINE = 1
__builtin__.ORDER_DROPOFF = 2
__builtin__.ORDER_ATTACK = 3
__builtin__.ORDER_DEFEND = 4
__builtin__.ORDER_FOLLOW = 5
__builtin__.ORDER_REACH = 6
__builtin__.ORDER_CONSTRUCT = 7
__builtin__.ORDER_REPAIR = 8
__builtin__.ORDER_FLEE = 9
__builtin__.ORDER_ENTERBUILDING = 10
__builtin__.ORDER_ENTERTRANSPORT = 11
__builtin__.ORDER_COMPLETED = 12
__builtin__.ORDER_ENTERMINE = 13

# Navigation Goal IDs (AIGOAL: obj->ai->goal->aigcs.goal)
__builtin__.GOAL_IDLE = 0
__builtin__.GOAL_GOTO = 1
__builtin__.GOAL_FOLLOW = 2
__builtin__.GOAL_FLEE = 3
__builtin__.GOAL_CONSTRUCT = 4
__builtin__.GOAL_MINE = 5
__builtin__.GOAL_ATTACKMELEE = 6
__builtin__.GOAL_ATTACKMISSILE = 7
__builtin__.GOAL_ATTACKPOUND = 8
__builtin__.GOAL_ATTACKSUICIDE = 9
__builtin__.GOAL_ENTERMINE = 10

# Navigation State IDs (TASK: obj->ai->goal->task)
__builtin__.STATE_NONE = 0
__builtin__.STATE_MOVING = 1
__builtin__.STATE_WAITING = 2

# Bot Names (For Samurai Wars: Names from Rurouni Kenshin and Ranma 1/2)
__builtin__.BOT_NAMES_LEGION = ['Beastslayer', 'Bravearmor', 'Grimpick', 'Doombellows', 'Shaletracker', 'Lockkiller',
                                'Deephunter', 'Goodpacer', 'Graverunner', 'Stonekiller', 'Bladesmither',
                                'Wraithtracker', 'Shalefighter', 'Blackcairn', 'Rockspirit', 'Goodgold']
__builtin__.BOT_NAMES_BEAST = ['Ogrunt', 'Ugfang', 'Skablug', 'Zodrunt', 'Shaksog', 'Waaog', 'Skarsnik', 'Uggul',
                               'Dregshak', 'Skumdreg', 'Wazgut', 'Mugdreg', 'Badog', 'Zoggog', 'Waagrub', 'Morskab']
__builtin__.BOT_NAMES_SAMURAI = ['Aoshi', 'Sanosuke', 'Kenshin', 'Yahiko', 'Shishio', 'Hajime', 'Kenshiro', 'Ryuken',
                                 'Raoh', 'Toki', 'Shin', 'Ranma', 'Ryoga', 'Genma', 'Kuno', 'Soun']
