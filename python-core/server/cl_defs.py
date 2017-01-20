# ---------------------------------------------------------------------------
#           Name: cl_defs.py
#         Author: Anthony Beaucamp (aka Mohican)
#  Last Modified: 13/03/2011
#    Description: Client-side Global Definitions
# ---------------------------------------------------------------------------

import __builtin__

# System Information
global gameTime

# Client Data Lists (for client.GetClientList)
global clientList_Name  # Client's Name
global clientList_UID  # Client's UID
global clientList_ClanID  # Client's Clan
global clientList_Race  # Client's Race
global clientList_Team  # Client's Team
global clientList_Squad  # Squad that Client belongs to
global clientList_Officer  # Is Client an Officer?
global clientList_Level  # Experience Level of Client
global clientList_UnitName  # Name of Client's Unit (string)
global clientList_UnitType  # Type of Client's Unit (integer)

# Game Information Types (for client.GetGameInfo)
__builtin__.GAME_TIME = 0  # Game Time (in msec)
__builtin__.GAME_STATE = 1  # Game State

# Client Information Types (for client.GetClientInfo)
__builtin__.CLIENT_UID = 0  # Client's UID (see cl_stats.py)
__builtin__.CLIENT_CLANID = 1  # Client's Clan ID

# General Data Information
__builtin__.MAX_LEVELS = 99  # Max levels in experience Table
