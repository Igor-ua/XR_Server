# ---------------------------------------------------------------------------
#           Name: cl_utils.py
#         Author: Anthony Beaucamp (aka Mohican)
#  Last Modified: 29/11/2011
#    Description: Useful routines and shared GUI commands
# ---------------------------------------------------------------------------

# Savage API
from core import *


def reformatDateTime(DateTime):
    # Reformat MySQL DateTime to a nice string
    if DateTime[5:7] == '01':
        DateTime = 'Jan' + DateTime[7:len(DateTime) - 3]
    elif DateTime[5:7] == '02':
        DateTime = 'Feb' + DateTime[7:len(DateTime) - 3]
    elif DateTime[5:7] == '03':
        DateTime = 'Mar' + DateTime[7:len(DateTime) - 3]
    elif DateTime[5:7] == '04':
        DateTime = 'Apr' + DateTime[7:len(DateTime) - 3]
    elif DateTime[5:7] == '05':
        DateTime = 'May' + DateTime[7:len(DateTime) - 3]
    elif DateTime[5:7] == '06':
        DateTime = 'Jun' + DateTime[7:len(DateTime) - 3]
    elif DateTime[5:7] == '07':
        DateTime = 'Jul' + DateTime[7:len(DateTime) - 3]
    elif DateTime[5:7] == '08':
        DateTime = 'Aug' + DateTime[7:len(DateTime) - 3]
    elif DateTime[5:7] == '09':
        DateTime = 'Sep' + DateTime[7:len(DateTime) - 3]
    elif DateTime[5:7] == '10':
        DateTime = 'Oct' + DateTime[7:len(DateTime) - 3]
    elif DateTime[5:7] == '11':
        DateTime = 'Nov' + DateTime[7:len(DateTime) - 3]
    else:
        DateTime = 'Dec' + DateTime[7:len(DateTime) - 3]

    return DateTime


def print_line(scroll, line, sel="", fmt="", buffered=1):
    ''' Print a line to a o_scrollbuffer '''
    cmd = 'o_scrollbuffer print %(Scroll)s "%(Line)s" "%(Sel)s" ' \
          % {"Scroll": scroll, "Line": line, 'Sel': sel}
    # if no fmt is entered, use the default one for sorting purposes
    if fmt != "":
        cmd += ' "%s" ' % fmt

    if buffered:
        CommandBuffer(cmd)
    else:
        CommandExec(cmd)


def GUI_show_popup(type='sb'):
    ''' Show Popup '''

    global popup_x, popup_y
    popup_x = CvarGetValue('int_mousepos_x') / CvarGetValue('gui_coordWidthMultiplier')
    popup_y = CvarGetValue('int_mousepos_y') / CvarGetValue('gui_coordHeightMultiplier')

    admin = getLoginInfo('ClanAdmin')
    UID = getLoginInfo('UID')
    CID = 0

    # list of all scrollbuffers being used
    scrollbuffers = ['buddies', 'members', 'members_mini', 'recruitment', 'search_clan', 'search_player', 'inbox']

    # type is a scrollbar
    if type == 'sb':
        name = CvarGetString('_selectedScrollBar')
    # type is a userlist
    elif type == 'ul':
        CommandExec('getSelectionUID; set _selectedID #answer#;')
        name = CvarGetString('_selectedUserList')
        # if no valid selection is made, don't show popup
        if int(CvarGetString('_selectedID')) == 0:
            return

    # unselect previous selected scrollbuffers
    for sb in scrollbuffers:
        if type == 'sb' and sb != name:
            CommandExec('o_scrollbuffer selectable %s_sb 0;' % sb)

    # init the popup panel
    command1 = 'set _i 1; \
        for _i 1 [_popup_numberButtons] 1 "hide popup_panel:lclk_button#_i#"; \
        panel focus popup_panel; '

    # list of all scrollbuffers that use popups
    if name == 'buddies':
        command2 = 'set _numberButtons 3; \
            select popup_panel:lclk_button1; \
                param text "Show Stats"; \
                param command "hide popup_panel; GUI_statsShow #_buddies_sb_variable#"; \
            select popup_panel:lclk_button2; \
                param text "Show Clan"; \
                param command "hide popup_panel; GUI_statsClanShow -1 #_buddies_sb_variable#"; \
            select popup_panel:lclk_button3; \
                param text "Send Email"; \
                param command "hide popup_panel; GUI_showComposeInbox #_buddies_sb_variable#"; '
        if CvarGetValue('_stats_UID') == UID:
            command2 = ''.join([command2, 'set _numberButtons 4; \
            select popup_panel:lclk_button4; \
                param text "Remove Buddy"; \
                param command "hide popup_panel; remBuddy #_buddies_sb_variable#; GUI_statsBuddies %i"; ' % UID])

    elif name == 'members':
        command2 = 'set _numberButtons 3; \
            select popup_panel:lclk_button1; \
                param text "Show Stats"; \
                param command "hide popup_panel; GUI_statsShow #_members_sb_variable#"; \
            select popup_panel:lclk_button2; \
                param text "Send Email"; \
                param command "hide popup_panel; GUI_showComposeInbox #_members_sb_variable#"; \
            select popup_panel:lclk_button3; \
                param text "Add Buddy"; \
                param command "hide popup_panel; addBuddy #_members_sb_variable#"; '
        if admin > 0:
            command2 = ''.join([command2, 'set _numberButtons 4; \
                select popup_panel:lclk_button4; \
                    param text "^yKick Player"; \
                    param command "hide popup_panel; GUI_showAreYouSure \"clanKick\" #_members_sb_variable#"; '])
        if admin > 1:
            command2 = ''.join([command2, 'set _numberButtons 7; \
                select popup_panel:lclk_button5; \
                    param text "^yPromote Admin"; \
                    param command "hide popup_panel; GUI_showAreYouSure \"clanPromoteAdmin\" #_members_sb_variable#"; \
                select popup_panel:lclk_button6; \
                    param text "^yDemote Admin"; \
                    param command "hide popup_panel; GUI_showAreYouSure \"clanDemoteAdmin\" #_members_sb_variable#"; \
                select popup_panel:lclk_button7; \
                    param text "^yTransfer leader"; \
                    param command "hide popup_panel; GUI_showAreYouSure \"clanTransferFounder\" #_members_sb_variable#";'])

    elif name == 'members_mini':
        command2 = 'set _numberButtons 3; \
            select popup_panel:lclk_button1; \
                param text "Show Stats"; \
                param command "hide popup_panel; GUI_statsShow #_members_mini_sb_variable#"; \
            select popup_panel:lclk_button2; \
                param text "Send Email"; \
                param command "hide popup_panel; GUI_showComposeInbox #_members_mini_sb_variable#"; \
            select popup_panel:lclk_button3; \
                param text "Add Buddy"; \
                param command "hide popup_panel; addBuddy #_members_mini_sb_variable#"; '

    elif name == 'recruitment':
        command2 = 'set _numberButtons 4; \
            select popup_panel:lclk_button1; \
                param text "Show Stats"; \
                param command "hide popup_panel; GUI_statsShow #_recruitment_sb_variable#"; \
            select popup_panel:lclk_button2; \
                param text "Send Email"; \
                param command "hide popup_panel; GUI_showComposeInbox #_recruitment_sb_variable#"; \
            select popup_panel:lclk_button3; \
                param text "Add Buddy"; \
                param command "hide popup_panel; addBuddy #_recruitment_sb_variable#"; \
            select popup_panel:lclk_button4; \
                param text "^yVote"; \
                param command "hide popup_panel; GUI_showVote #_recruitment_sb_variable#"; '
        if admin >= 1:
            command2 = ''.join([command2, 'set _numberButtons 6; \
                select popup_panel:lclk_button5; \
                    param text "^yInvite player"; \
                    param command "hide popup_panel; GUI_showAreYouSure \"clanInvite\" #_recruitment_sb_variable#"; \
                select popup_panel:lclk_button6; \
                    param text "^yDeny application"; \
                    param command "hide popup_panel; GUI_showAreYouSure \"clanRemoveApplication\" #_recruitment_sb_variable#;"; '])

    elif name == 'history':
        command2 = ''

    elif name == 'history_mini':
        command2 = ''

    elif name == 'shoutbox':
        command2 = ''
        # 'set _numberButtons 2; \
        # select popup_panel:lclk_button1; param text "Send Email"; \
        # select popup_panel:lclk_button1; param command "hide popup_panel; \
        # GUI_showComposeInbox #_shoutbox_sb_variable#"; \
        # select popup_panel:lclk_button2; param text "Delete PM"; \
        # select popup_panel:lclk_button2; param command "hide popup_panel; \
        # GUI_removeShout #_shoutbox_sb_variable#";'

    elif name == 'search_clan':
        command2 = 'set _numberButtons 2; \
            select popup_panel:lclk_button1; \
                param text "Show Clan"; \
                param command "hide popup_panel; GUI_statsClanShow #_search_clan_sb_variable# -1"; \
            select popup_panel:lclk_button2; \
                param text "Join Clan"; \
                param command "hide popup_panel; GUI_showApplyClan #_search_clan_sb_variable#"; '
        # if admin > 0:
        #    command2 = ''.join([command2, 'set _numberButtons 3; \
        #        select popup_panel:lclk_button3; \
        #            param text "^yChallenge Clan"; \
        #            param command "hide popup_panel"; '])
        # TODO: implement challenging clan

    elif name == 'search_player':
        command2 = 'set _numberButtons 4; \
            select popup_panel:lclk_button1; \
                param text "Show Stats"; \
                param command "hide popup_panel; GUI_statsShow #_search_player_sb_variable#"; \
            select popup_panel:lclk_button2; \
                param text "Show Clan"; \
                param command "hide popup_panel; GUI_statsClanShow -1 #_search_player_sb_variable#"; \
            select popup_panel:lclk_button3; \
                param text "Send Email"; \
                param command "hide popup_panel; GUI_showComposeInbox #_search_player_sb_variable#"; \
            select popup_panel:lclk_button4; \
                param text "Add Buddy"; \
                param command "hide popup_panel; addBuddy #_search_player_sb_variable#"; '
        if admin > 0:
            command2 = ''.join([command2, 'set _numberButtons 5; \
                select popup_panel:lclk_button5; \
                    param text "^yInvite player"; \
                    param command "hide popup_panel; clanInvite #_search_player_sb_variable#"; '])

    elif name == 'inbox':
        command2 = ''

    elif name == 'whos_online':
        command2 = 'set _numberButtons 4; \
            select popup_panel:lclk_button1; \
                param text "Show Stats"; \
                param command "hide popup_panel; GUI_statsShow #_whos_online_sb_variable#"; \
            select popup_panel:lclk_button2; \
                param text "Show Clan"; \
                param command "hide popup_panel; GUI_statsClanShow -1 #_whos_online_sb_variable#"; \
            select popup_panel:lclk_button3; \
                param text "Send Email"; \
                param command "hide popup_panel; GUI_showComposeInbox #_whos_online_sb_variable#"; \
            select popup_panel:lclk_button4; \
                param text "Add Buddy"; \
                param command "hide popup_panel; addBuddy #_whos_online_sb_variable#"; '
        if admin > 0:
            command2 = ''.join([command2, 'set _numberButtons 5; \
                select popup_panel:lclk_button5; \
                    param text "^yInvite player"; \
                    param command "hide popup_panel; clanInvite #_whos_online_sb_variable#"; '])

    # list of all userlists who use popups
    elif name in ['team0_userlist_names', 'team1_members', 'team2_members', 'team3_members', 'team4_members']:
        command2 = 'set _numberButtons 4; \
            select popup_panel:lclk_button1; \
                param text "Show Stats"; \
                param command "hide popup_panel; GUI_statsShow #_selectedID#"; \
            select popup_panel:lclk_button2; \
                param text "Show Clan"; \
                param command "hide popup_panel; GUI_statsClanShow -1 #_selectedID#"; \
            select popup_panel:lclk_button3; \
                param text "Send Email"; \
                param command "hide popup_panel; GUI_showComposeInbox #_selectedID#"; \
            select popup_panel:lclk_button4; \
                param text "Add Buddy"; \
                param command "hide popup_panel; addBuddy #_selectedID#"; '
        if admin > 0:
            command2 = ''.join([command2, 'set _numberButtons 5; \
                select popup_panel:lclk_button5; \
                    param text "^yInvite player"; \
                    param command "hide popup_panel; clanInvite #_selectedID#"; '])

    # present the popup panel
    command3 = 'panel move popup_panel [int_mousepos_x / gui_coordWidthMultiplier] [int_mousepos_y / gui_coordHeightMultiplier]; \
        set _i 1; for _i 1 [_numberButtons] 1 "show popup_panel:lclk_button#_i#"; \
        panel focus popup_panel; '

    # put it all together and execute
    CommandExec(''.join([command1, command2, command3]))


def GUI_hide_popup():
    ''' Hide Popup '''
    popup_buttons = CvarGetValue('_numberButtons')
    x = CvarGetValue('int_mousepos_x') / CvarGetValue('gui_coordWidthMultiplier')
    y = CvarGetValue('int_mousepos_y') / CvarGetValue('gui_coordHeightMultiplier')
    w = CvarGetValue('_popup_button_width')
    h = CvarGetValue('_popup_button_height') * popup_buttons
    xx = popup_x
    yy = popup_y

    if (x > xx + w) or (x < xx) or (y < yy) or (y > yy + h):
        CommandExec('hide popup_panel')
