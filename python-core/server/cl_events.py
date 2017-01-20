# ---------------------------------------------------------------------------
#           Name: cl_events.py
#         Author: Anthony Beaucamp (aka Mohican)
#  Last Modified: 11/03/2011
#    Description: Silverback Event Entries (init, frame)
# ---------------------------------------------------------------------------

# Savage API
from core import *
import client

# Savage Modules
import cl_defs
import cl_clans
import cl_maps
import cl_stats
import cl_utils

# Python Modules
import time


# -------------------------------
# Called directly by Silverback
# -------------------------------
def init():
    # Print Console Message
    ConsolePrint('Python: Initializing Client-Side...\n')

    # Initialize some Variables
    global update_next_time
    update_next_time = time.clock()

    try:
        # Register various Console Commands
        RegisterCmd("login", "cl_events", "login")
        RegisterCmd("register", "cl_events", "register")
        RegisterCmd("addShout", "cl_events", "addShout")
        RegisterCmd("getShouts", "cl_events", "getShouts")
        RegisterCmd("getClientInfo", "cl_events", "getClientInfo")
        RegisterCmd("printClientInfo", "cl_events", "printClientInfo")
        RegisterCmd("printMOTD", "cl_events", "printMOTD")

        RegisterCmd("login_GUI", "cl_events", "GUI_login")
        RegisterCmd("register_GUI", "cl_events", "GUI_register")
        RegisterCmd("GUI_update", "cl_events", "GUI_update")

        RegisterCmd('GUI_showPopup', 'cl_utils', 'GUI_show_popup')
        RegisterCmd('GUI_hidePopup', 'cl_utils', 'GUI_hide_popup')

        # Init other Client Modules
        cl_clans.init()
        cl_maps.init()
        cl_stats.init()

    except:
        # Print Error Message
        ConsolePrint('Python: Initialization FAILED!\n')


# -------------------------------
# Called directly by Silverback
# -------------------------------
def reload():
    # Print Console Message
    ConsolePrint('Python: Reloading Client-Side...\n')

    # Fetch Map Stats for GUI
    cl_maps.GUI_getMapInfo(CvarGetString('world_name'))


# -------------------------------
# Called directly by Silverback
# -------------------------------
def frame():
    try:
        # Refresh System Information
        cl_defs.gameTime = client.GetGameInfo(GAME_TIME)

        # Refresh Client Data
        [cl_defs.clientList_Name, cl_defs.clientList_UID, cl_defs.clientList_ClanID,
         cl_defs.clientList_Race, cl_defs.clientList_Team, cl_defs.clientList_Squad,
         cl_defs.clientList_Officer, cl_defs.clientList_Level, cl_defs.clientList_UnitName,
         cl_defs.clientList_UnitType] = client.GetClientList()

    except:
        pass


# -------------------------------
# Called directly by Silverback
# -------------------------------
def update():
    # Check Client is logged in!
    if getLoginInfo('UID') == 0:
        return

    # Only from time-to-time
    global update_next_time
    if time.clock() < update_next_time:
        return
    update_next_time = time.clock() + 120

    # Spawn update Thread
    createThread('import cl_events; cl_events.update_thread()')


def GUI_update():
    # Check Client is logged in!
    if getLoginInfo('UID') == 0:
        return

    # Post-pone next automatic update
    global update_next_time
    update_next_time = time.clock() + 120

    # Spawn update Thread
    createThread('import cl_events; cl_events.update_thread()')


def update_thread():
    # Contact Authentication server
    info = Client_GetStatus()
    if 'Error' in info:
        ConsolePrint(info['Error'])

    # Refresh who's online ScrollBuffer
    CommandBuffer('o_scrollbuffer clear whos_online_scrollbuffer')
    for i in range(len(info['listUID'])):
        # Print in scrollbuffer
        if info['listClanID'][i] != 0:
            CommandBuffer('o_scrollbuffer print whos_online_scrollbuffer \
                            "^w%(Abbrev)s^w^clan %(CID)d^%(Name)s" \
                            "%(UID)s"' \
                          % {'Abbrev': info['listClanAbbrev'][i], \
                             'CID': info['listClanID'][i], \
                             'Name': info['listName'][i], \
                             'UID': info['listUID'][i]})
        else:
            CommandBuffer('o_scrollbuffer print whos_online_scrollbuffer \
                            "%(Name)s" "%(UID)s"' \
                          % {'Name': info['listName'][i], \
                             'UID': info['listUID'][i]})

    # Check that Notifications are enabled
    if CvarGetValue('cl_notifyEmails') > 0:
        # Update Emails Overlay
        CvarSetValue('emails_new', info['emailsNew'])
        CvarSetString('emails_text', '%i' % info['emailsNew'])
        CommandBuffer('select emails_notification_panel:count; param text "%i"' % info['emailsNew'])


# -------------------------------
# Login Commands
# -------------------------------
def login(username, password=-1):
    # Use Threads to prevent hanging the Application
    password = getLoginInfo('Password') if password == -1 else password
    createThread('import cl_events; cl_events.login_thread("%s", "%s")' % (username, password))


def login_thread(username, password):
    # Attempt Account Login
    info = Client_Login(username, password)

    # Refresh Game State
    if 'Error' in info:
        ConsolePrint(info['Error'])
        return
    elif 'Down' in info:
        CommandExec(
            'show error_panel; textbuffer clear error_panel:error_explanation; textbuffer print error_panel:error_explanation "%s"' %
            info['Down'])
        ConsolePrint(info['Down'])
        return

    # Print Information
    ConsolePrint(info['Info'])


def GUI_login(username, password):
    # Use Threads to prevent hanging the Application
    info = Client_Login(username, password)

    # Refresh Game State
    if 'Error' in info:
        CommandExec(
            'show error_panel; textbuffer clear error_panel:error_explanation; textbuffer print error_panel:error_explanation "%s"' %
            info['Error'])
        return
    elif 'Down' in info:
        CommandExec('uiState normal; hideall; show menu_panel')
        CommandExec(
            'show error_panel; textbuffer clear error_panel:error_explanation; textbuffer print error_panel:error_explanation "%s"' %
            info['Down'])
        return

    # Show Main Menu
    CommandExec('uiState normal; hideall; show menu_panel')


def register(username, password):
    # Use Threads to prevent hanging the Application
    createThread('import cl_events; cl_events.register_thread("%s", "%s")' % (username, password))


def register_thread(username, password):
    # Attempt Account Login
    info = Client_Register(username, password)

    # Refresh Game State
    if 'Error' in info:
        ConsolePrint(info['Error'])
        return
    elif 'Down' in info:
        CommandExec(
            'show error_panel; textbuffer clear error_panel:error_explanation; textbuffer print error_panel:error_explanation "%s"' %
            info['Down'])
        ConsolePrint(info['Down'])
        return

    # Print Information
    ConsolePrint(info['Info'])


def GUI_register(username, password):
    # Use Threads to prevent hanging the Application
    info = Client_Register(username, password)

    # Refresh Game State
    if 'Error' in info:
        CommandExec(
            'show error_panel; textbuffer clear error_panel:error_explanation; textbuffer print error_panel:error_explanation "%s"' %
            info['Error'])
        return
    elif 'Down' in info:
        CommandExec('uiState normal; hideall; show menu_panel')
        CommandExec(
            'show error_panel; textbuffer clear error_panel:error_explanation; textbuffer print error_panel:error_explanation "%s"' %
            info['Down'])
        return

    # Show Main Menu
    CommandExec('uiState normal; hideall; show menu_panel')


# -------------------------------
# Info Commands
# -------------------------------
def getClientInfo(key):
    # Get Info from built-in Login Function
    CvarSetString('answer', str(getLoginInfo(key)))


def printClientInfo():
    # Print Login Info
    ConsolePrint('Username: %s\n' % getLoginInfo('Username'))
    ConsolePrint('UID/ClanID: %i/%i\n' % (getLoginInfo('UID'), getLoginInfo('ClanID')))
    ConsolePrint('Buddies: %s\n' % str(getLoginInfo('Buddies')))


def printMOTD():
    # Clear MOTD
    CommandBuffer('scrollbuffer clear motd_scrollbuffer')

    # Print all Lines (MOTD is a builtin)
    for line in MOTD:
        CommandBuffer('scrollbuffer print motd_scrollbuffer "%s"' % str(line))

        # -------------------------------


# Shoutbox Commands
# -------------------------------
def addShout(message):
    if message[0] == '/' or message[1] == '/':
        CommandExec(
            'show error_panel; textbuffer clear error_panel:error_explanation; textbuffer print error_panel:error_explanation "Do you think the public shoutbox is a good place to accidentally reveal your password or private messages? It isn\'t, so don\'t use any /commands."')
        return

    # Use Threads to prevent hanging the Application
    createThread('import cl_events; cl_events.addShout_thread("%s")' % message)


def addShout_thread(message):
    # Try to post Shout
    info = Client_AddShout(message)

    # Was it succesfully?
    if 'Error' in info:
        CommandExec(
            'show error_panel; textbuffer clear error_panel:error_explanation; textbuffer print error_panel:error_explanation "%s"' %
            info['Error'])
    else:
        getShouts()


def getShouts():
    # Use Threads to prevent hanging the Application
    createThread('import cl_events; cl_events.getShouts_thread()')


def getShouts_thread():
    # Add latest shouts
    ID = CvarGetValue('public_shouts_ID')
    shouts = Client_GetShouts(ID)

    # Was it succesfully?
    if 'Error' in shouts:
        return

    # Print into the various ScrollBuffers
    for i in range(len(shouts['listUID']) - 1, -1, -1):
        # Reformat Date-Time
        DateTime = cl_utils.reformatDateTime(shouts['listDateTime'][i])

        # DEBUGGING
        # ConsolePrint('\"^w%(Abbrev)s^w %(CID)d%(Name)s"\n' \
        #                    % {'Abbrev': shouts['listClanAbbrev'][i], \
        #                       'CID': shouts['listClanID'][i], 'Name': shouts['listName'][i]})

        # Print in scrollbuffer
        # CLEMENS: Hack to exclude clanID 0, because clan0 suddenly seems to exist and mess it up...
        if shouts['listClanID'][i] == 0:
            CommandBuffer('scrollbuffer print public_shouts_scrollbuffer \
                        "^980[%(Date)s] ^w%(Name)s^w: %(Message)s"' \
                          % {'Date': DateTime, \
                             'Name': shouts['listName'][i], \
                             'Message': shouts['listMessage'][i]})
        else:
            CommandBuffer('scrollbuffer print public_shouts_scrollbuffer \
                        "^980[%(Date)s] ^w%(Abbrev)s^w^clan %(CID)d^%(Name)s^w: %(Message)s"' \
                          % {'Date': DateTime, 'Abbrev': shouts['listClanAbbrev'][i], \
                             'CID': shouts['listClanID'][i], 'Name': shouts['listName'][i], \
                             'Message': shouts['listMessage'][i]})

    # Scroll to last line
    CommandBuffer('scrollbuffer scroll public_shouts_scrollbuffer 9999')

    # Update 'public_shouts_ID'
    CvarSetValue('public_shouts_ID', shouts['listID'][0])
