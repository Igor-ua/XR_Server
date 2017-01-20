# ---------------------------------------------------------------------------
#           Name: cl_clans.py
#         Author: Xavier Rasschaert (aka Faith)
#  Last Modified: __DATE__
#    Description: Download and display Clan information
# ---------------------------------------------------------------------------

# Savage API
from core import *

# Python Library Modules
import sys
import gui

# Savage Modules
import cl_utils


def init():
    ''' Register various console commands '''
    try:

        init_globals()

        # clan commands
        RegisterCmd('clanCreate', 'cl_clans', 'clan_create')
        RegisterCmd('clanLeave', 'cl_clans', 'clan_leave')
        RegisterCmd('clanPromoteAdmin', 'cl_clans', 'clan_promote_admin')
        RegisterCmd('clanDemoteAdmin', 'cl_clans', 'clan_demote_admin')
        RegisterCmd('clanTransferFounder', 'cl_clans', 'clan_transfer_founder')
        RegisterCmd('clanKick', 'cl_clans', 'clan_kick')
        RegisterCmd('clanChangeName', 'cl_clans', 'clan_change_name')
        RegisterCmd('clanChangeAbbrev', 'cl_clans', 'clan_change_abbrev')
        RegisterCmd('clanChangeMotto', 'cl_clans', 'clan_change_motto')
        RegisterCmd('clanChangeStatus', 'cl_clans', 'clan_change_status')
        RegisterCmd('clanChangeDifficulty', 'cl_clans', 'clan_change_difficulty')
        RegisterCmd('clanChangeTemplate', 'cl_clans', 'clan_change_template')
        RegisterCmd('clanApply', 'cl_clans', 'clan_apply')

        # TODO: add invitation / application commands
        RegisterCmd('clanIcon', 'cl_clans', 'clan_icon')
        RegisterCmd('clanBanner', 'cl_clans', 'clan_banner')
        RegisterCmd('clanInvite', 'cl_clans', 'clan_invite')
        RegisterCmd('clanUninvite', 'cl_clans', 'clan_uninvite')
        RegisterCmd('clanListInvitations', 'cl_clans', 'clan_list_invitations')
        RegisterCmd('clanAcceptInvitation', 'cl_clans', 'clan_accept_invitation')
        RegisterCmd('clanDeclineInvitation', 'cl_clans', 'clan_decline_invitation')
        RegisterCmd('clanUnsendApplication', 'cl_clans', 'clan_unsend_application')
        RegisterCmd('clanRemoveApplication', 'cl_clans', 'clan_remove_application')
        RegisterCmd('clanMembers', 'cl_clans', 'clan_members')
        RegisterCmd('clanCommands', 'cl_clans', 'clan_commands')
        RegisterCmd('clanHelp', 'cl_clans', 'clan_help')

        # legacy clan commands
        RegisterCmd('createclan', 'cl_clans', 'legacy_createclan')
        RegisterCmd('leaveclan', 'cl_clans', 'legacy_leaveclan')
        RegisterCmd('newicon', 'cl_clans', 'legacy_newicon')
        RegisterCmd('invite', 'cl_clans', 'legacy_invite')
        RegisterCmd('joinclan', 'cl_clans', 'legacy_joinclan')
        RegisterCmd('kickfromclan', 'cl_clans', 'legacy_kickfromclan')
        RegisterCmd('makeclanadmin', 'cl_clans', 'legacy_makeclanadmin')
        RegisterCmd('transfersuperadmin', 'cl_clans', 'legacy_transfersuperadmin')
        RegisterCmd('userkickfromclan', 'cl_clans', 'legacy_userkickfromclan')
        RegisterCmd('usermakeclanadmin', 'cl_clans', 'legacy_usermakeclanadmin')
        RegisterCmd('usertransfersuperadmin', 'cl_clans', 'legacy_usertransfersuperadmin')

        # open up a specific tab
        RegisterCmd('clanPanel', 'cl_clans', 'clan_panel')
        RegisterCmd('competitionPanel', 'cl_clans', 'competition_panel')
        RegisterCmd('searchPanel', 'cl_clans', 'search_panel')
        RegisterCmd('inboxPanel', 'cl_clans', 'inbox_panel')

        # commands to be used for GUI control
        RegisterCmd('GUI_showClanInfo', 'cl_clans', 'GUI_show_my_clan')
        RegisterCmd('GUI_showCompetitionInfo', 'cl_clans', 'GUI_show_competition_info')
        RegisterCmd('GUI_showSearchInfo', 'cl_clans', 'GUI_show_search_info')
        RegisterCmd('GUI_showInboxInfo', 'cl_clans', 'GUI_show_inbox_info')
        RegisterCmd('GUI_showInboxMessage', 'cl_clans', 'GUI_show_inbox_message')
        RegisterCmd('GUI_showComposeInbox', 'cl_clans', 'GUI_show_compose_inbox')
        RegisterCmd('GUI_clanCreate', 'cl_clans', 'GUI_clan_create')
        RegisterCmd('GUI_showAreYouSure', 'cl_clans', 'GUI_show_are_you_sure')
        RegisterCmd('GUI_search', 'cl_clans', 'GUI_search')
        RegisterCmd('GUI_statsClanShow', 'cl_clans', 'GUI_stats_clan_show')
        RegisterCmd('GUI_shout', 'cl_clans', 'GUI_shout')
        RegisterCmd('GUI_removeShout', 'cl_clans', 'GUI_remove_shout')
        RegisterCmd('GUI_recruitmentDiscussion', 'cl_clans', 'GUI_recruitment_discussion')
        RegisterCmd('GUI_showVote', 'cl_clans', 'GUI_show_vote')
        RegisterCmd('GUI_vote', 'cl_clans', 'GUI_vote')
        RegisterCmd('GUI_clanApply', 'cl_clans', 'GUI_clan_apply')
        RegisterCmd('GUI_showApplyClan', 'cl_clans', 'GUI_show_apply_clan')
        RegisterCmd('GUI_manageClan', 'cl_clans', 'GUI_manage_clan')
        RegisterCmd('GUI_showManageClan', 'cl_clans', 'GUI_show_manage_clan')
        RegisterCmd('GUI_sendPM', 'cl_clans', 'GUI_send_PM')
        RegisterCmd('GUI_readPM', 'cl_clans', 'GUI_read_PM')
        RegisterCmd('GUI_replyPM', 'cl_clans', 'GUI_reply_PM')
        RegisterCmd('GUI_deletePM', 'cl_clans', 'GUI_delete_PM')
    except:
        ConsolePrint('Error registering clan managment commands...\n')


def init_globals():
    # keep a reference to the current running threads
    global thread_clan, thread_competition, thread_search, thread_inbox
    global thread_miniclan, thread_search_action, thread_areyousure
    thread_clan = None
    thread_competition = None
    thread_search = None
    thread_inbox = None
    thread_miniclan = None
    thread_search_action = None
    thread_areyousure = None

    # who do you want to send the smail to?
    global send_UID
    # what clan do you want to join?
    global join_CID
    # who are we voting for (clanApplication)?
    global vote_UID


def clan_panel():
    global thread_clan
    if not (thread_clan == None) and thread_clan.isAlive():
        return
    thread_clan = createThread("import cl_clans; cl_clans.clan_panel_thread()")


def clan_panel_thread():
    CommandBuffer("show clanManagmentpanel; show clanmenu_panel; \
            show clan_panel; hide competition_panel; hide search_panel; hide inbox_panel; \
            hide popup_panel; hide inbox_read_panel;hide inbox_interactive_panel; \
            select clan_button; param text_color 1 .8 0; \
            select competition_button; param text_color 1 1 1; \
            select search_button; param text_color 1 1 1; \
            select inbox_button; param text_color 1 1 1; ")

    GUI_show_my_clan()
    GUI_refresh_inbox_button()


def competition_panel():
    global thread_competition
    if not (thread_competition == None) and thread_competition.isAlive():
        return
    thread_competition = createThread("import cl_clans; cl_clans.competition_panel_thread()")


def competition_panel_thread():
    CommandExec("show clanManagmentpanel; show clanmenu_panel; \
            show competition_panel; hide clan_panel; hide search_panel; hide inbox_panel; \
            hide popup_panel; hide inbox_read_panel;hide inbox_interactive_panel; \
            select clan_button; param text_color 1 1 1; \
            select competition_button; param text_color 1 .8 0; \
            select search_button; param text_color 1 1 1; \
            select inbox_button; param text_color 1 1 1; \
            hide manageclan_button")

    GUI_show_competition_info()
    GUI_refresh_inbox_button()


def search_panel():
    global thread_search
    if not (thread_search == None) and thread_search.isAlive():
        return
    thread_search = createThread("import cl_clans; cl_clans.search_panel_thread()")


def search_panel_thread():
    CommandExec("show clanManagmentpanel; show clanmenu_panel; \
            show search_panel; hide clan_panel; hide competition_panel; hide inbox_panel; \
            hide popup_panel; hide inbox_read_panel;hide inbox_interactive_panel; \
            select clan_button; param text_color 1 1 1; \
            select competition_button; param text_color 1 1 1; \
            select search_button; param text_color 1 .8 0; \
            select inbox_button; param text_color 1 1 1; \
            hide manageclan_button")

    GUI_show_search_info()
    GUI_refresh_inbox_button()


def inbox_panel():
    global thread_inbox
    if not (thread_inbox == None) and thread_inbox.isAlive():
        return
    thread_inbox = createThread("import cl_clans; cl_clans.inbox_panel_thread()")


def inbox_panel_thread():
    CommandExec("show clanManagmentpanel; show clanmenu_panel; \
            show inbox_panel; hide clan_panel; hide competition_panel; hide search_panel; \
            hide popup_panel; show inbox_read_panel; \
            select clan_button; param text_color 1 1 1; \
            select competition_button; param text_color 1 1 1; \
            select search_button; param text_color 1 1 1; \
            select inbox_button; param text_color 1 .8 0; \
            hide manageclan_button")

    GUI_show_inbox_info()
    GUI_refresh_inbox_button()


def clan_create(Abbrev, Name):
    info = Clan_Create(Abbrev, Name)
    ConsolePrint('%s\n' % info)
    return info


def clan_leave(refreshGUI=0):
    info = Clan_Leave()
    if refreshGUI:
        GUI_show_my_clan()
    CommandBuffer('login %s %s' % (getLoginInfo('Username'), getLoginInfo('Password')))  # hack to reload icon
    ConsolePrint('%s\n' % info)
    return info


def clan_promote_admin(UID, refreshGUI=0):
    info = Clan_Manage({'promoteAdmin': int(float(UID))})
    if 'Error' in info:
        CommandExec(
            'show error_panel; textbuffer clear error_panel:error_explanation; textbuffer print error_panel:error_explanation "%s"' %
            info['Error'])
        CommandExec('focus error_panel')
        return
    if refreshGUI:
        GUI_show_my_clan()
    ConsolePrint('%s\n' % info)
    return info


def clan_demote_admin(UID, refreshGUI=0):
    info = Clan_Manage({'demoteAdmin': int(float(UID))})
    if 'Error' in info:
        CommandExec(
            'show error_panel; textbuffer clear error_panel:error_explanation; textbuffer print error_panel:error_explanation "%s"' %
            info['Error'])
        CommandExec('focus error_panel')
        return
    if refreshGUI:
        GUI_show_my_clan()
    ConsolePrint('%s\n' % info)
    return info


def clan_transfer_founder(UID, refreshGUI=0):
    info = Clan_Manage({'transferFounder': int(float(UID))})
    if 'Error' in info:
        CommandExec(
            'show error_panel; textbuffer clear error_panel:error_explanation; textbuffer print error_panel:error_explanation "%s"' %
            info['Error'])
        CommandExec('focus error_panel')
        return
    CommandBuffer(
        'login %s %s' % (CvarGetString('username'), CvarGetString('password')))  # hack to reload admin status
    if refreshGUI:
        GUI_show_my_clan()
    ConsolePrint('%s\n' % info)
    return info


def clan_kick(UID, refreshGUI=0):
    info = Clan_Manage({'kickPlayer': int(float(UID))})
    if 'Error' in info:
        CommandExec(
            'show error_panel; textbuffer clear error_panel:error_explanation; textbuffer print error_panel:error_explanation "%s"' %
            info['Error'])
        CommandExec('focus error_panel')
        return
    if refreshGUI:
        GUI_show_my_clan()
    ConsolePrint('%s\n' % info)
    return info


def clan_change_name(name):
    info = Clan_Manage({'changeName': name})
    ConsolePrint('%s\n' % info)
    return info


def clan_change_abbrev(abbrev):
    info = Clan_Manage({'changeAbbrev': abbrev})
    ConsolePrint('%s\n' % info)
    return info


def clan_change_motto(motto):
    info = Clan_Manage({'changeMotto': motto})
    ConsolePrint('%s\n' % info)
    return info


def clan_change_status(status):
    info = Clan_Manage({'changeStatus': status})
    ConsolePrint('%s\n' % info)
    return info


def clan_change_difficulty(diff):
    info = Clan_Manage({'changeDifficulty': diff})
    ConsolePrint('%s\n' % info)
    return info


def clan_change_template(temp):
    info = Clan_Manage({'changeTemplate': temp})
    ConsolePrint('%s\n' % info)
    return info


def clan_apply(ClanID, Message):
    info = Clan_SendApplication(ClanID, Message)
    ConsolePrint('%s\n' % info)
    return info


def clan_icon(filename):
    info = Clan_Manage({'changeIcon': filename})
    CommandExec('flushclanicon %i' % getLoginInfo('ClanID'))
    CommandExec('cacheclanicon %i' % getLoginInfo('ClanID'))
    ConsolePrint('%s\n' % info)
    return info


def clan_banner(filename):
    info = Clan_Manage({'changeBanner': filename})
    CommandExec('flushgraphicurl "%s%i.jpg"' % (CvarGetString('clan_banner_url'), getLoginInfo('ClanID')))
    CommandExec('cachegraphicurl "%s%i.jpg"' % (CvarGetString('clan_banner_url'), getLoginInfo('ClanID')))
    ConsolePrint('%s\n' % info)
    return info


def clan_invite(UID, refreshGUI=0):
    info = Clan_SendInvitation(int(float(UID)))
    if refreshGUI:
        GUI_show_my_clan()
    ConsolePrint('%s\n' % info)
    return info


def clan_uninvite(UID):
    info = Clan_UnsendInvitation(int(float(UID)))
    ConsolePrint('%s\n' % info)
    return info


def clan_list_invitations():
    info = Clan_GetClientInvitations()
    ConsolePrint('%s\n' % info)
    return info


def clan_accept_invitation(CID):
    info = Clan_AcceptInvitation(int(float(CID)))
    if 'Error' in info:
        CommandExec(
            'show error_panel; textbuffer clear error_panel:error_explanation; textbuffer print error_panel:error_explanation "%s"' %
            info['Error'])
        CommandExec('focus error_panel')
        return
    CommandBuffer('login %s %s' % (getLoginInfo('Username'), getLoginInfo('Password')))  # hack to reload icon
    ConsolePrint('%s\n' % info)
    return info


def clan_decline_invitation(CID):
    info = Clan_DeclineInvitation(int(float(CID)))
    ConsolePrint('%s\n' % info)
    return info


def clan_unsend_application(CID):
    info = Clan_UnsendApplication(int(float(CID)))
    ConsolePrint('%s\n' % info)
    return info


def clan_remove_application(UID, refreshGUI=0):
    info = Clan_RemoveApplication(int(float(UID)))
    if refreshGUI:
        GUI_show_my_clan()
    ConsolePrint('%s\n' % info)
    return info


def clan_members(ClanID=0):
    if ClanID == 0:
        ClanID = getLoginInfo('ClanID')
    if ClanID == 0:
        return
    info = Clan_GetInfo(ClanID)
    nr_members = len(info['listUID'])
    for i in range(nr_members):
        if info['listAdmin'][i] == 0:
            clr = '^g'
        elif info['listAdmin'][i] == 1:
            clr = '^b'
        elif info['listAdmin'][i] == 2:
            clr = '^y'
        ConsolePrint('%(Color)s%(Member)s^w(%(Nick)s)[%(UID)d]' \
                     % {'Member': info['listUsername'][i], 'Nick': info['listNameMostUsed'][i],
                        'UID': info['listUID'][i], 'Color': clr})
        if i != nr_members - 1:
            ConsolePrint(', ')
        else:
            ConsolePrint('\n')
    return info


def clan_commands():
    # mark the commands by color to describe the status in clan needed to use that command
    # y: everyone, g: only members, 900: admin
    commands = ['^yclanCreate', '^gclanLeave', '^900clanIcon', '^gclanMembers', '^900clanPromoteAdmin', \
                '^900clanDemoteAdmin', '^900clanTransferFounder', '^900clanKick', '^900clanChangeName', \
                '^900clanChangeAbbrev', '^900clanChangeMotto', '^900clanChangeStatus', '^900clanChangeDifficulty', \
                '^yclanApply', '^900clanInvite', '^900clanUninvite', '^yclanUnsendApplication', \
                '^900ClanRemoveApplication', '^yclanPanel', '^yClanAcceptInvitation']

    # sort the commands
    commands.sort()
    commands.reverse()

    # print commands to console
    for i in range(len(commands)):
        ConsolePrint(commands[i] + '\n')


def clan_help():
    # Display some help
    ConsolePrint('Type "clanCommands" to see the list of clan commands.\n')
    ConsolePrint('To get started, you can use "clanCreate <abbrev> <name>".\n')


def GUI_send_PM(ID):
    global send_UID

    subj = CvarGetString('inbox_compose_subject')
    to = int(float(send_UID))
    mes = CvarGetString('_inbox_compose_ta_variable')
    info = Client_SendEmail(to, subj, mes)
    print_info(info, GUI_show_inbox_info, 'inbox_info')
    if not ('Error' in info):
        gui.Hide('inbox_compose_panel')


def GUI_read_PM(ID):
    mail = Client_GetEmail(ID)
    CommandBuffer('o_scrollbuffer clear inbox_read_sb')
    print_line(scroll='inbox_read_sb', line=mail['Message'])


def GUI_reply_PM(ID):
    if len(ID) > len('MESS_') and ID[:len('MESS_')] == 'MESS_':
        MID = int(ID[len('MESS_'):])
    else:
        print_info("can't reply to this mail!", GUI_show_inbox_info, 'inbox_info')
        return
    mes = Client_GetInbox()
    if not ('Info' in mes):
        index = (mes['listID']).index(MID)
        UID = (mes['listUID'])[index]
        CvarSetString('inbox_compose_to', str(UID))
    CvarSetString('inbox_compose_subject', 'Re: ' + (mes['listSubject'])[index])
    GUI_show_compose_inbox(UID)


def GUI_delete_PM(ID):
    if len(ID) > len('MESS_') and ID[:len('MESS_')] == 'MESS_':
        MID = int(ID[len('MESS_'):])
    else:
        print_info("can't delete this mail!", GUI_show_inbox_info, 'inbox_info')
        return
    info = Client_DeleteEmail(MID)
    print_info(info, GUI_show_inbox_info, 'inbox_info')


def GUI_show_compose_inbox(UID):
    global send_UID
    send_UID = UID

    gui.Focus('inbox_compose_panel')
    info = Client_GetInfo(int(float(UID)))
    CvarSetString('_inbox_compose_ta_variable', '')
    CommandExec('select inbox_compose_panel:portrait; param url "%s%s.jpg"' % (CvarGetString('user_portrait_url'), UID))
    if not ('Error' in info):
        gui.Param('inbox_compose_panel:inbox_compose_to_lbl', 'text',
                  'To: %s^w^clan %s^%s' % (info['ClanAbbrev'], info['ClanID'], info['NameMostUsed']))


def GUI_refresh_inbox_button():
    status = Client_GetStatus()
    gui.Param('inbox_button', 'text', 'Inbox(%s/%s)' % (status['emailsNew'], status['emailsCount']))


def GUI_clan_create(Abbrev, Name):
    info = clan_create(Abbrev, Name)
    if 'Info' in info:
        CommandExec('panel hide createclan_dialog_panel')
    print_info(info, GUI_show_my_clan, 'createclan_info', 'clan_info')


def GUI_remove_shout(ID):
    ConsolePrint('STRING:%s\n' % ID)
    info = Clan_RemShout(int(float(ID)))
    print_info(info, GUI_show_my_clan, 'clan_info')


def GUI_clan_apply():
    try:
        ClanID = CvarGetValue('_search_clan_sb_variable')
        message = CvarGetString('_apply_about_ta_variable')
        info = Clan_SendApplication(int(float(ClanID)), message)
        CommandExec('panel hide applyclan_dialog_panel')
        if 'Error' in info:
            CommandExec(
                'show error_panel; textbuffer clear error_panel:error_explanation; textbuffer print error_panel:error_explanation "%s"' %
                info['Error'])
            CommandExec('focus error_panel')
            return
        GUI_refresh_inbox_button()
    except:
        # Print Error Message
        error = 'Python: Error parsing gui clan apply\n'
        error = error + '%s%s\n' % (sys.exc_info()[0], sys.exc_info()[1])
        ConsolePrint(error)


def GUI_vote(vote, UID):
    try:
        if vote:
            info = Clan_VoteApplicationYes(int(UID))
        else:
            info = Clan_VoteApplicationNo(int(UID))
        print_info(info, GUI_show_my_clan, 'clan_info')
    except:
        # Print Error Message
        error = 'Python: Error parsing gui vote\n'
        error = error + '%s%s\n' % (sys.exc_info()[0], sys.exc_info()[1])
        ConsolePrint(error)


def GUI_manage_clan():
    createThread('import cl_clans; cl_clans.GUI_manage_clan_thread()')


def GUI_manage_clan_thread():
    try:
        ClanID = getLoginInfo('ClanID')
        admin = getLoginInfo('ClanAdmin')
        info = Clan_GetInfo(ClanID)

        if admin == 0:
            CommandBuffer('panel hide manage_clan_panel')
            return

        if 'Error' in info:
            print_info(info, None, 'clan_info', 'manageclan_info')
            return

        query = {}
        name = CvarGetString('manageclan_name')
        if name != info['ClanName']:
            query['changeName'] = name
        abbrev = CvarGetString('manageclan_abbrev')
        if abbrev != info['ClanAbbrev']:
            query['changeAbbrev'] = abbrev
        icon = CvarGetString('manageclan_icon')
        if icon != "":
            clan_icon(icon)
        motto = CvarGetString('manageclan_motto')
        if motto != info['ClanMotto']:
            query['changeMotto'] = motto
        status = CvarGetValue('manage_status_mode')
        if status != info['ClanStatus']:
            query['changeStatus'] = status
        diff = CvarGetValue('manage_diff_mode')
        if diff != info['ClanDifficulty']:
            query['changeDifficulty'] = diff
        vote_perc = CvarGetValue('manageclan_vote')
        # not implemented
        auto_add = CvarGetValue('manage_add_apps')
        # not implemented
        temp = CvarGetString('_manage_apply_about_ta_variable')
        if temp != info['ClanTemplate']:
            query['changeTemplate'] = temp
        banner = CvarGetString('manageclan_banner')
        ConsolePrint('%s\n' % banner)
        if banner != "":
            clan_banner(banner)
        if len(query) == 0:
            print_line(scroll='manageclan_info', line="^900You didn't make any changes")
        info = Clan_Manage(query)
        if 'Info' in info:
            CommandBuffer('panel hide manage_clan_panel')
        print_info(info, GUI_show_my_clan, 'clan_info', 'manageclan_info')
    except:
        # Print Error Message
        error = 'Python: Error parsing manage clan\n'
        error = error + '%s%s\n' % (sys.exc_info()[0], sys.exc_info()[1])
        ConsolePrint(error)


def GUI_show_clan_info(panel, ClanID, clan_info):
    ''' Fill in information of the clan info o_scrollbuffer '''
    CommandBuffer('o_scrollbuffer clear %(Panel)s; o_scrollbuffer selectable %(Panel)s 0' \
                  % {'Panel': panel})
    index = (clan_info['listAdmin']).index(2)
    claninfo_leader = (clan_info['listNameMostUsed'])[index]
    nr_members = len(clan_info['listUID'])
    ClanStatus = clan_info['ClanStatus']
    if ClanStatus == 0:
        claninfo_status = 'Frozen'
    elif ClanStatus == 1:
        claninfo_status = 'Closed'
    elif ClanStatus == 2:
        claninfo_status = 'Recruiting, difficulty: %s' \
                          % progress(int(clan_info['ClanDifficulty']) * 20)
    print_line(scroll=panel,
               line=' ^yClan name: ^w%(Abbrev)s^w^clan %(ID)s^ ^wa.k.a %(Name)s ^col^' \
                    % {'ID': ClanID, 'Abbrev': clan_info['ClanAbbrev'], 'Name': clan_info['ClanName']})
    print_line(scroll=panel,
               line=(' ^yClan Founder: ^w%(Abbrev)s^w^clan %(ID)s^%(Leader)s' \
                     % {'Abbrev': clan_info['ClanAbbrev'], 'ID': ClanID, 'Leader': claninfo_leader}) +
                    '^w with %(Nr)d member%(S)s^col^' % {'Nr': nr_members,
                                                         'S': '' if nr_members == 1 else 's'})
    print_line(scroll=panel, line=' ^yClan motto: ^w%(Motto)s ^col^' \
                                  % {'Motto': clan_info['ClanMotto']})
    print_line(scroll=panel, line=' ^yClan status: ^w%(Status)s ^col^' \
                                  % {'Status': claninfo_status})
    print_line(scroll=panel, line=' ^yUpcoming match: ^w%(NOT)s ^col^' \
                                  % {'NOT': '^900None'})

    avg_clan_kills = clan_info['ClanKills'] * 1.0 / nr_members
    avg_clan_deaths = clan_info['ClanDeaths'] * 1.0 / nr_members
    if avg_clan_deaths > 0:
        ratio_kills = round(avg_clan_kills / avg_clan_deaths, 3)
    else:
        ratio_kills = 0.0

    print_line(scroll=panel, line=(' ^yAvg. Kills/deaths:  ^g%(Kills)d^w/^r%(Deaths)d' \
                                   % {'Kills': int(avg_clan_kills),
                                      'Deaths': int(avg_clan_deaths)}) + ' ^w(%(Ratio).2f) ^col^' \
                                                                         % {'Ratio': ratio_kills})

    avg_clan_game_wins = clan_info['ClanGameWins'] * 1.0 / nr_members
    avg_clan_game_losses = clan_info['ClanGameLosses'] * 1.0 / nr_members
    if avg_clan_game_losses > 0:
        ratio_game_wins = round(avg_clan_game_wins / avg_clan_game_losses, 3)
    else:
        ratio_game_wins = 0.0

    print_line(scroll=panel, line=' ^yAvg. Game wins/losses: ' +
                                  ' ^g%(Wins)d^w/^r%(Losses)d ^w(%(Ratio).2f) ^col^' \
                                  % {'Wins': int(avg_clan_game_wins), 'Losses': int(avg_clan_game_losses),
                                     'Ratio': ratio_game_wins})

    avg_clan_comm_wins = clan_info['ClanCommWins'] * 1.0 / nr_members
    avg_clan_comm_losses = clan_info['ClanCommLosses'] * 1.0 / nr_members
    if avg_clan_comm_losses > 0:
        ratio_comm_wins = round(avg_clan_comm_wins / avg_clan_comm_losses, 3)
    else:
        ratio_comm_wins = 0.0

    print_line(scroll=panel, line=' ^yAvg. Commander wins/losses: ' +
                                  ' ^g%(Wins)s^w/^r%(Losses)s ^w(%(Ratio).2f) ^col^' \
                                  % {'Wins': int(avg_clan_comm_wins), 'Losses': int(avg_clan_comm_losses),
                                     'Ratio': ratio_comm_wins})


def GUI_show_members_info(panel, ClanID, clan_info):
    ''' Fill in information of the member info o_scrollbuffer '''
    claninfo_nr_members = len(clan_info['listUID'])
    CommandBuffer('o_scrollbuffer clear %(Panel)s; o_scrollbuffer selectable %(Panel)s 0' \
                  % {'Panel': panel})
    for i in range(claninfo_nr_members):
        if clan_info['listAdmin'][i] == 0:
            status = 'Member'
        elif clan_info['listAdmin'][i] == 1:
            status = '^bAdmin'
        elif clan_info['listAdmin'][i] == 2:
            status = '^yFounder'
        UID = clan_info['listUID'][i]
        print_line(scroll=panel, line='%(Abbrev)s^w^clan %(ClanID)s^%(Name)s^col^%(Status)s^col^%(LastSeen)s^col^' \
                                      % {'Abbrev': clan_info['ClanAbbrev'], 'ClanID': ClanID,
                                         'Name': escape(clan_info['listNameMostUsed'][i]), 'Status': status,
                                         'LastSeen': clan_info['listLastSeen'][i]},
                   sel=str(clan_info['listUID'][i]),
                   fmt='%(Name)s ^col^%(Status)d ^col^%(LastSeen)d ^col^' \
                       % {'Name': clan_info['listNameMostUsed'][i], 'Status': clan_info['listAdmin'][i],
                          'LastSeen': clan_info['listLastSeenInt'][i]})
    CommandBuffer('o_scrollbuffer param %s sort_column 1; o_scrollbuffer param %s sort_column 1' % (panel, panel))


def GUI_show_recruitment_info(panel, clan_info, clan_apps):
    ClanID = getLoginInfo('ClanID')

    claninfo_nr_members = len(clan_info['listUID'])
    for i in range(len(clan_apps['listUID'])):
        UID = clan_apps['listUID'][i]
        name = clan_apps['listName'][i]
        yes = clan_apps['listVoteYes'][i]
        no = clan_apps['listVoteNo'][i]
        progr = progress(int(100 * float(yes) / float(claninfo_nr_members)))
        # TODO: * perc_votes_needed
        print_line(scroll=panel, line='%(Name)s^col^%(Progress)s^col^%(F1)s^col^%(F2)s^col^' \
                                      % {'F1': yes, 'F2': no, 'Name': name, 'Progress': progr}, sel=str(UID))


def GUI_show_shoutbox(panel, clan_info, shouts):
    ClanID = getLoginInfo('ClanID')

    if not ('Info' in shouts):
        for i in range(len(shouts['listID'])):
            ID = shouts['listID'][i]
            UID = shouts['listUID'][i]
            CID = ClanID
            index = (clan_info['listUID']).index(UID)
            name = (clan_info['listNameMostUsed'])[index]
            abbrev = clan_info['ClanAbbrev']
            mes = shouts['listMessage'][i]
            date = cl_utils.reformatDateTime(shouts['listDateTime'][i])
            print_line(scroll=panel, line='[%(Date)s] %(Abbrev)s^w^clan %(CID)d^%(Name)s^w: %(Mes)s^col^' \
                                          % {'Date': date, 'Abbrev': abbrev, 'CID': CID, 'Name': name, 'Mes': mes},
                       sel=str(ID),
                       fmt='%s ^col^' % date)


def GUI_show_my_clan():
    ''' Fill in information of the clan tab '''
    try:
        ClanID = getLoginInfo('ClanID')
        admin = int(getLoginInfo('ClanAdmin'))

        # clear data of old clan info, so it is empty while downloading data
        CommandExec('o_scrollbuffer clear %(Panel)s; o_scrollbuffer selectable %(Panel)s 0' \
                    % {'Panel': 'claninfo_sb'})
        CommandExec('o_scrollbuffer clear %(Panel)s; o_scrollbuffer selectable %(Panel)s 0' \
                    % {'Panel': 'members_sb'})
        CommandExec('o_scrollbuffer clear %(Panel)s; o_scrollbuffer selectable %(Panel)s 0' \
                    % {'Panel': 'recruitment_sb'})
        CommandExec('o_scrollbuffer clear %(Panel)s; o_scrollbuffer selectable %(Panel)s 0' \
                    % {'Panel': 'shoutbox_sb'})

        # Refresh Clan Banner
        CommandExec('select clan_panel:banner; param url "%s%i.jpg"' % (CvarGetString('clan_banner_url'), ClanID))

        # Show Clan Manage Button?
        if admin > 0:
            CommandExec('show manageclan_button')
        else:
            CommandExec('hide manageclan_button')

        if ClanID == 0:
            print_line(scroll='claninfo_sb', line=' ^900You are currently not in a clan,')
            print_line(scroll='claninfo_sb', line=' ^900either join a clan or change username')
        else:
            # get the necessary data
            clan_info = Clan_GetInfo(ClanID)
            clan_apps = Clan_GetClanApplications()
            shouts = Clan_GetShouts()

            # claninfo buffer
            GUI_show_clan_info('claninfo_sb', ClanID, clan_info)
            # members buffer
            GUI_show_members_info('members_sb', ClanID, clan_info)
            # recruitment buffer
            GUI_show_recruitment_info('recruitment_sb', clan_info, clan_apps)
            # shoutbox buffer
            GUI_show_shoutbox('shoutbox_sb', clan_info, shouts)

        GUI_refresh_inbox_button()
    except:
        # Print Error Message
        error = 'Python: Error parsing Clan Info\n'
        error = error + '%s%s\n' % (sys.exc_info()[0], sys.exc_info()[1])
        ConsolePrint(error)

    # Always keep error messages in the fore-front
    CommandExec('isvisible error_panel answer')
    if CvarGetValue('answer'):
        CommandExec('focus error_panel')


def GUI_show_competition_info():
    ''' Fill in information of the competition tab '''
    try:
        GUI_refresh_inbox_button()
    except:
        # Print Error Message
        error = 'Python: Error parsing Competition Info\n'
        error = error + '%s%s\n' % (sys.exc_info()[0], sys.exc_info()[1])
        ConsolePrint(error)

    # Always keep error messages in the fore-front
    CommandExec('isvisible error_panel answer')
    if CvarGetValue('answer'):
        CommandExec('focus error_panel')


def GUI_show_search_info():
    ''' Fill in information of the Search tab '''
    try:
        search_mode = CvarGetString('search_mode')
        if search_mode == 'player_name':
            gui.Hide('search_clan_sb')
            gui.Show('search_player_sb')
        else:
            gui.Show('search_clan_sb')
            gui.Hide('search_player_sb')
        GUI_refresh_inbox_button()
    except:
        # Print Error Message
        error = 'Python: Error parsing Search Info\n'
        error = error + '%s%s\n' % (sys.exc_info()[0], sys.exc_info()[1])
        ConsolePrint(error)

    # Always keep error messages in the fore-front
    CommandExec('isvisible error_panel answer')
    if CvarGetValue('answer'):
        CommandExec('focus error_panel')


def GUI_get_clan_applications():
    ClanID = getLoginInfo('ClanID')
    clan_apps = Clan_GetClanApplications()
    color = '^w'
    for i in range(len(clan_apps['listUID'])):
        UID = clan_apps['listUID'][i]
        name = clan_apps['listName'][i]
        yes = clan_apps['listVoteYes'][i]
        no = clan_apps['listVoteNo'][i]
        date = cl_utils.reformatDateTime(clan_apps['listDateTime'][i])
        subj = '%(Color)s%(Name)s wants to join our Clan' % {'Color': color, 'Name': name}
        print_line(scroll='inbox_sb', line='%(Color)s%(Name)s^col^%(Color)s%(Date)s^col^%(Subject)s^col^' \
                                           % {'Color': color, 'Name': name, 'Date': date, 'Subject': subj},
                   sel='CLAN_APP_' + str(UID),
                   fmt='%s ^col^ %s ^col^ %s ^col^' % (name, clan_apps['listDateTime'][i], subj))


def GUI_get_client_applications():
    color = '^w'
    client_apps = Clan_GetClientApplications()
    for i in range(len(client_apps['listClanID'])):
        CID = client_apps['listClanID'][i]
        name = client_apps['listClanName'][i]
        abbrev = client_apps['listClanAbbrev'][i]
        mes = client_apps['listMessage'][i]
        date = cl_utils.reformatDateTime(client_apps['listDateTime'][i])
        subj = '%(Color)sYour application was send to %(Abbrev)s^w^clan %(ClanID)d^' % {'Color': color,
                                                                                        'Abbrev': abbrev, 'ClanID': CID}
        print_line(scroll='inbox_sb', line='%(Color)s%(Name)s^col^%(Color)s%(Date)s^col^%(Subject)s^col^' \
                                           % {'Color': color, 'Name': name, 'Date': date, 'Subject': subj},
                   sel='CLIENT_APP_' + str(CID),
                   fmt='%s ^col^ %s ^col^ %s ^col^' % (name, client_apps['listDateTime'][i], subj))


def GUI_get_client_invitations():
    color = '^g'
    clan_invs = Clan_GetClientInvitations()
    for i in range(len(clan_invs['listClanID'])):
        CID = clan_invs['listClanID'][i]
        info = Clan_GetInfo(CID)
        if 'Error' not in info:
            abbrev = info['ClanAbbrev']
            date = cl_utils.reformatDateTime(clan_invs['listDateTime'][i])
            subj = '%(Color)sYou are invited to join %(Abbrev)s^w^clan %(ClanID)d^' % {'Color': color, 'Abbrev': abbrev,
                                                                                       'ClanID': CID}
            print_line(scroll='inbox_sb', line='%(Color)s%(Name)s^col^%(Color)s%(Date)s^col^%(Subject)s^col^' \
                                               % {'Color': color, 'Name': abbrev, 'Date': date, 'Subject': subj},
                       sel='CLAN_INV_' + str(CID),
                       fmt='%s ^col^ %s ^col^ %s ^col^' % (abbrev, clan_invs['listDateTime'][i], subj))


def GUI_get_inbox():
    color = '^090'
    mes = Client_GetInbox()
    if not ('Info' in mes):
        for i in range(len(mes['listID'])):
            ID = mes['listID'][i]
            UID = mes['listUID'][i]
            name = mes['listName'][i]
            CID = mes['listClanID'][i]
            abbrev = mes['listClanAbbrev'][i]
            subj = mes['listSubject'][i]
            date = cl_utils.reformatDateTime(mes['listDateTime'][i])
            check = mes['listChecked'][i]
            color = '^g' if not (check) else ''
            print_line(scroll='inbox_sb',
                       line='%(Abbrev)s^w^clan %(ClanID)s^%(Color)s%(Name)s^col^%(Color)s%(Date)s^col^%(Color)s%(Subject)s^col^' \
                            % {'Color': color, 'Name': name, 'Date': date, 'Abbrev': abbrev, 'ClanID': CID,
                               'Subject': subj}, sel='MESS_' + str(ID),
                       fmt='%s ^col^%s ^col^%s ^col^' % (name, mes['listDateTime'][i], subj))


def GUI_show_inbox_info():
    ''' Fill in information of the inbox tab '''
    try:
        gui.Hide('inbox_interactive_panel')
        CommandExec(' \
            o_scrollbuffer clear inbox_sb; \
            o_scrollbuffer selectable inbox_sb 0;')
        CommandExec('o_scrollbuffer clear inbox_read_sb')
        CommandExec('select inbox_panel:portrait; param url ""')

        # TODO: make date sortable
        GUI_get_client_invitations()
        GUI_get_client_applications()
        GUI_get_clan_applications()
        GUI_get_inbox()

        # show most recent mails first
        CommandExec('o_scrollbuffer param inbox_sb sort_column 1;o_scrollbuffer param inbox_sb sort_column 1;')
        GUI_refresh_inbox_button()

    except:
        # Print Error Message
        error = 'Python: Error parsing Inbox Info\n'
        error = error + '%s%s\n' % (sys.exc_info()[0], sys.exc_info()[1])
        ConsolePrint(error)

        # Always keep error messages in the fore-front
    CommandExec('isvisible error_panel answer')
    if CvarGetValue('answer'):
        CommandExec('focus error_panel')


def GUI_show_inbox_message():
    createThread('import cl_clans; cl_clans.GUI_show_inbox_message_thread()')


def GUI_show_inbox_message_thread():
    CommandBuffer('o_scrollbuffer clear inbox_read_sb')
    ID = CvarGetString('_inbox_sb_variable')
    if len(ID) > len('MESS_') and ID[:len('MESS_')] == 'MESS_':
        gui.Hide('inbox_interactive_panel')
        ID = int(ID[len('MESS_'):])
        GUI_read_PM(ID)
        mes = Client_GetInbox()
        index = (mes['listID']).index(ID)
        UID = (mes['listUID'])[index]
        CommandBuffer('select inbox_panel:portrait; param url "%s%s.jpg"' % (CvarGetString('user_portrait_url'), UID))
    elif len(ID) > len('CLAN_APP_') and ID[:len('CLAN_APP_')] == 'CLAN_APP_':
        gui.Param('inbox_i_label', 'text', 'Do you want to vote?')
        gui.Hide('inbox_i_button1')
        gui.Hide('inbox_i_button2')
        gui.Param('inbox_i_buttonc', 'text', 'Vote')
        gui.Param('inbox_i_buttonc', 'command', 'GUI_showVote %s' % ID[len('CLAN_APP_'):])
        gui.Show('inbox_i_buttonc')
        gui.Focus('inbox_interactive_panel')
    elif len(ID) > len('CLIENT_APP_') and ID[:len('CLIENT_APP_')] == 'CLIENT_APP_':
        gui.Param('inbox_i_label', 'text', 'Do you want to cancel?')
        gui.Hide('inbox_i_button1')
        gui.Hide('inbox_i_button2')
        gui.Param('inbox_i_buttonc', 'text', 'Unsend Application')
        gui.Param('inbox_i_buttonc', 'command', 'clanUnsendApplication %s; GUI_showInboxInfo' % ID[len('CLIENT_APP_'):])
        gui.Show('inbox_i_buttonc')
        gui.Focus('inbox_interactive_panel')
        gui.Focus('inbox_interactive_panel')
    elif len(ID) > len('CLAN_INV_') and ID[:len('CLAN_INV_')] == 'CLAN_INV_':
        gui.Param('inbox_i_label', 'text', 'Do you want to accept?')
        gui.Hide('inbox_i_buttonc')
        gui.Show('inbox_i_button1')
        gui.Param('inbox_i_button1', 'text', 'Accept')
        gui.Param('inbox_i_button1', 'command', 'ClanAcceptInvitation %s; GUI_showInboxInfo' % ID[len('CLAN_INV_'):])
        gui.Show('inbox_i_button2')
        gui.Param('inbox_i_button2', 'text', 'Decline')
        gui.Param('inbox_i_button2', 'command', 'ClanDeclineInvitation %s; GUI_showInboxInfo' % ID[len('CLAN_INV_'):])
        gui.Focus('inbox_interactive_panel')


def GUI_show_apply_clan(ClanID=-1):
    createThread('import cl_clans; cl_clans.GUI_show_apply_clan_thread(%s)' % ClanID)


def GUI_show_apply_clan_thread(ClanID):
    global join_CID

    if ClanID == -1:
        ClanID = join_CID

    clan_info = Clan_GetInfo(int(float(ClanID)))
    CommandBuffer('panel focus applyclan_dialog_panel; \
        select applyclan_dialog_label; param text "Application for clan ^clan %(ID)i^^w%(Name)s";'
                  % {'ID': ClanID, 'Name': clan_info['ClanName'], "Template": clan_info['ClanTemplate']})
    CvarSetString('_apply_about_ta_variable', clan_info['ClanTemplate'])
    CommandBuffer(
        'select applyclan_dialog_panel:banner; param url "%s%i.jpg"' % (CvarGetString('clan_banner_url'), ClanID))


def GUI_show_are_you_sure(cmd, ID):
    global thread_areyousure
    if not (thread_areyousure == None) and thread_areyousure.isAlive():
        return
    thread_areyousure = createThread("import cl_clans; cl_clans.GUI_show_are_you_sure_thread('%s', %s)" % (cmd, ID))


def GUI_show_are_you_sure_thread(cmd, ID):
    info = Client_GetInfo(int(ID))
    ClanID = getLoginInfo('ClanID')
    gui.Focus('areyousure_dialog_panel')

    if cmd == "clanLeave":
        if ClanID != 0:
            gui.Param('areyousure_dialog_label', 'text', 'Are you sure you want to leave this Clan?')
            gui.Param('areyousure_dialog_yes_button', 'command', '%s 1; hide areyousure_dialog_panel' % cmd)
            return
        else:
            gui.Hide('areyousure_dialog_panel')
    elif cmd == "clanKick":
        gui.Param('areyousure_dialog_label', 'text',
                  'Are you sure you want to kick %(Name)s?' % {'Name': info['NameMostUsed']})
    elif cmd == "clanPromoteAdmin":
        gui.Param('areyousure_dialog_label', 'text',
                  'Are you sure you want to promote %(Name)s?' % {'Name': info['NameMostUsed']})
    elif cmd == "clanDemoteAdmin":
        gui.Param('areyousure_dialog_label', 'text',
                  'Are you sure you want to demote %(Name)s?' % {'Name': info['NameMostUsed']})
    elif cmd == "clanTransferFounder":
        gui.Param('areyousure_dialog_label', 'text',
                  'Are you sure you want to transfer founder to %(Name)s?' % {'Name': info['NameMostUsed']})
    elif cmd == "clanInvite":
        gui.Param('areyousure_dialog_label', 'text',
                  'Are you sure you want to invite %(Name)s?' % {'Name': info['NameMostUsed']})
    elif cmd == "clanRemoveApplication":
        gui.Param('areyousure_dialog_label', 'text',
                  'Are you sure you want to deny the application of %(Name)s?' % {'Name': info['NameMostUsed']})

    gui.Param('areyousure_dialog_yes_button', 'command', '%s %s 1; hide areyousure_dialog_panel' % (cmd, ID))


def GUI_show_manage_clan():
    ClanID = getLoginInfo('ClanID')
    if ClanID != 0:
        createThread('import cl_clans; cl_clans.GUI_show_manage_clan_thread()')


def GUI_show_manage_clan_thread():
    ClanID = getLoginInfo('ClanID')
    clan_info = Clan_GetInfo(ClanID)

    gui.Focus('manage_clan_panel')
    manage_diff_modes = ['Very easy - Noob clan',
                         'Easy - Noob friendly clan',
                         'Medium - Normal clan',
                         'Hard - Pro clan',
                         'Very hard - 1337 clan']
    manage_status_modes = ['Frozen - Clan not active',
                           'Closed - Not Recruiting',
                           'Recruiting - Accepting']
    CommandBuffer('panel focus manage_clan_panel; \
        menu clear manage_diff_menu; \
        menu clear manage_status_menu; \
        textbuffer clear manageclan_info;')
    gui.Param('manageclan_icon_label', 'text', 'Icon:^clan %(ClanID)i^ , Path:' % {'ClanID': ClanID})
    # CommandBuffer('label param manageclan_icon_label text "Icon:^clan %(ClanID)i^ , Path:"' \
    #    % {'ClanID': ClanID})
    for i in range(5):
        CommandBuffer('menu add manage_diff_menu \"%(Name)s\" "set manage_diff_mode %(Index)d";' \
                      % {'Name': manage_diff_modes[i], 'Index': i + 1})
    for i in range(3):
        CommandBuffer('menu add manage_status_menu \"%(Name)s\" "set manage_status_mode %(Index)d";' \
                      % {'Name': manage_status_modes[i], 'Index': i})
    CvarSetString('manageclan_name', clan_info['ClanName'])
    CvarSetString('manageclan_abbrev', clan_info['ClanAbbrev'])
    CvarSetString('manageclan_motto', clan_info['ClanMotto'])
    CvarSetString('_manage_apply_about_ta_variable', clan_info['ClanTemplate'])
    CommandBuffer('menu select manage_diff_menu "%s"' \
                  % manage_diff_modes[clan_info['ClanDifficulty'] - 1])
    CommandBuffer('menu select manage_status_menu "%s"' \
                  % manage_status_modes[clan_info['ClanStatus']])

    CvarSetValue('manage_add_apps', 0)  # not implemented yet on SS
    CvarSetString('manageclan_vote', '50')  # not implemented yet on SS

    # Refresh Clan Banner
    CommandBuffer('select manage_clan_panel:banner; param url "%s%i.jpg"' % (
    CvarGetString('clan_banner_url'), getLoginInfo('ClanID')))


def GUI_shout():
    createThread('import cl_clans; cl_clans.GUI_shout_thread()')


def GUI_shout_thread():
    ''' Add shout to shoutbox '''
    try:
        shout_msg = CvarGetString('shout_msg')
        info = Clan_AddShout(shout_msg)
        if 'Error' in info:
            ConsolePrint('error in shouting:%s' % info)
        CommandBuffer('GUI_showClanInfo')
    except:
        # Print Error Message
        error = 'Python: Error parsing Shout Info\n'
        error = error + '%s%s\n' % (sys.exc_info()[0], sys.exc_info()[1])
        ConsolePrint(error)


def GUI_recruitment_discussion():
    createThread('import cl_clans; cl_clans.GUI_recruitment_discussion_thread()')


def GUI_recruitment_discussion_thread():
    ''' Add text to recruitment discussion '''
    try:
        global vote_UID
        msg = CvarGetString('recruitment_discussion_msg')
        info = Clan_AddApplicationShout(vote_UID, msg)
        if 'Error' in info:
            ConsolePrint('error in shouting:%s' % info)
        CommandBuffer('GUI_showVote %s' % vote_UID)
        # TODO: implement
    except:
        # Print Error Message
        error = 'Python: Error parsing Shout Info\n'
        error = error + '%s%s\n' % (sys.exc_info()[0], sys.exc_info()[1])
        ConsolePrint(error)


def GUI_show_vote(UID):
    createThread('import cl_clans; cl_clans.GUI_show_vote_thread(%d)' % int(float(UID)))


def GUI_show_vote_thread(UID):
    ''' Show Vote '''
    try:
        global vote_UID
        vote_UID = UID
        ClanID = getLoginInfo('ClanID')
        app_info = Clan_GetClanApplications()
        clan_info = Clan_GetInfo(ClanID)
        nr_members = len(clan_info['listUID'])
        index = (app_info['listUID']).index(UID)

        # vote panel
        name = (app_info['listName'])[index]
        msg = (app_info['listMessage'])[index]
        yes = (app_info['listVoteYes'])[index]
        no = (app_info['listVoteNo'])[index]
        date = cl_utils.reformatDateTime((app_info['listDateTime'])[index])
        vote_need = 0.75  # TODO
        green = yes * 1.0 / nr_members
        red = no * 1.0 / nr_members
        gui.Param('recruitment_vote_yes_button', 'command', 'hide recruitment_vote_panel; GUI_vote 1 %d' % UID)
        gui.Param('recruitment_vote_no_button', 'command', 'hide recruitment_vote_panel; GUI_vote 0 %d' % UID)
        CommandBuffer('show recruitment_vote_panel; panel focus recruitment_vote_panel; \
            select recruitment_vote_panel:recruitment_vote_seconds_text; param text \
            "Votes needed: ?%%"; \
            select recruitment_vote_panel:recruitment_vote_yes_text; param text "F1 or Yes: %(Yes)d"; \
            select recruitment_vote_panel:recruitment_vote_no_text; param text "F2 or No: %(No)d"; \
            select recruitment_vote_panel:recruitment_vote_topic; param text "Recruiting: %(Name)s"; \
            select recruitment_vote_panel:recruitment_vote_areyousure_text; param text \
            "Do you want %(Name)s to join your clan ^clan %(ClanID)d^ ?"; \
            set recruitment_vote_need 0.75; \
            set recruitment_vote_greensize %(Green)f; \
            set recruitment_vote_redsize %(Red)f; ' \
                      % {"Yes": yes, "No": no, "Name": name, "ClanID": ClanID, "Green": green, "Red": red})

        # application shouts    
        shouts = Clan_GetApplicationShouts(UID)
        ConsolePrint('%s' % shouts)
        CommandBuffer('o_scrollbuffer clear vote_discussion_sb')
        if not ('Info' in shouts):
            for i in range(len(shouts['listID'])):
                ID = shouts['listID'][i]
                UID = shouts['listUID'][i]
                CID = ClanID
                index = (clan_info['listUID']).index(UID)
                name = (clan_info['listNameMostUsed'])[index]
                abbrev = clan_info['ClanAbbrev']
                mes = shouts['listMessage'][i]
                date = cl_utils.reformatDateTime(shouts['listDateTime'][i])
                print_line(scroll='vote_discussion_sb',
                           line='[%(Date)s] %(Abbrev)s^w^clan %(CID)d^%(Name)s^w: %(Mes)s^col^' \
                                % {'Date': date, 'Abbrev': abbrev, 'CID': CID, 'Name': name, 'Mes': mes}, sel=str(ID),
                           fmt='%s ^col^' % date)
        CommandBuffer('o_scrollbuffer selectable vote_discussion_sb 0;')

        # about scrollbuffer   
        CommandBuffer('o_scrollbuffer clear about_sb')
        print_text('about_sb', msg)
    except:
        # Print Error Message
        error = 'Python: Error parsing Vote Info\n'
        error = error + '%s%s\n' % (sys.exc_info()[0], sys.exc_info()[1])
        ConsolePrint(error)


def GUI_search():
    global thread_search_action
    if not (thread_search_action == None) and thread_search_action.isAlive():
        return
    thread_search_action = createThread("import cl_clans; cl_clans.GUI_search_thread()")


def GUI_search_thread():
    ''' Search player name or clan name '''
    try:
        search = CvarGetString('search_string')
        search_mode = CvarGetString('search_mode')

        if search_mode == 'clan_name':
            CommandExec('o_scrollbuffer clear search_clan_sb; o_scrollbuffer selectable search_clan_sb 0')
            membersMin = int(CvarGetValue('membersmin_input'))
            membersMax = int(CvarGetValue('membersmax_input'))
            range_min = int(CvarGetValue('rangemin_input'))
            range_max = int(CvarGetValue('rangemax_input'))
            status = int(CvarGetValue('search_clan_status'))
            search_info = Clan_Search(
                {'abbrev': search, 'status': status, 'membersMin': membersMin, 'membersMax': membersMax,
                 'rangeMin': range_min, 'rangeMax': range_max})
            if 'Error' in search_info:
                return
            CommandExec(
                'label param searchresults_label text "The search found %d matches"' % len(search_info['listClanID']))
            for i in range(len(search_info['listClanStatus'])):
                ClanStatus = search_info['listClanStatus'][i]
                if ClanStatus == 0:
                    claninfo_status = 'Inactive (frozen)'
                elif ClanStatus == 1:
                    claninfo_status = 'Active (not recruiting)'
                elif ClanStatus == 2:
                    claninfo_status = ''.join(
                        ['Recruiting, difficulty: ', progress(int(search_info['listClanDifficulty'][i]) * 20)])
                Clan_ID = search_info['listClanID'][i]
                Abbrev = search_info['listClanAbbrev'][i]
                Name = search_info['listClanName'][i]
                NumMembers = search_info['listClanNumMembers'][i]
                comm = '?'
                kills = '?'
                print_line(scroll='search_clan_sb',
                           line='%(Abbrev)s^w^clan %(ClanID)s^^col^%(Name)s^col^%(Status)s^col^%(NumMembers)s^col^%(Kills)s^col^%(Comm)s^col^' \
                                % {'Abbrev': Abbrev, 'ClanID': Clan_ID, 'Name': Name, 'Status': claninfo_status,
                                   'NumMembers': NumMembers, 'Kills': kills, 'Comm': comm}, sel=Clan_ID)
            # sort on the status column so players can find a recruiting clan
            CommandExec(
                'o_scrollbuffer param search_clan_sb sort_column 2; o_scrollbuffer param search_clan_sb sort_column 2')
        elif search_mode == 'player_name':
            CommandExec('o_scrollbuffer clear search_player_sb; o_scrollbuffer selectable search_player_sb 0')
            range_min = int(CvarGetValue('rangemin_input'))
            range_max = int(CvarGetValue('rangemax_input'))
            search_info = Client_Search({'name': search, 'rangeMin': range_min, 'rangeMax': range_max})
            if 'Error' in search_info:
                return
            CommandExec(
                'label param searchresults_label text "The search found %d matches"' % len(search_info['listUID']))
            for i in range(len(search_info['listUID'])):
                ConsolePrint('info:%s\n' % search_info)
                UID = search_info['listUID'][i]
                Clan_ID = search_info['listClanID'][i]
                Abbrev = search_info['listClanAbbrev'][i]
                Name = search_info['listName'][i]
                lastSeen = '?'
                comm = '?/?'
                kills = '?/?'
                killstreak = '?'
                playtime = '?'
                print_line(scroll='search_player_sb',
                           line='%(Abbrev)s^w^clan %(ClanID)s^^col^%(Name)s^col^%(LastSeen)s^col^%(Playtime)s^col^%(Killstreak)s^col^%(Kills)s^col^%(Comm)s^col^' \
                                % {'Abbrev': Abbrev, 'ClanID': Clan_ID, 'Name': Name, 'LastSeen': lastSeen,
                                   'Playtime': playtime, 'Killstreak': killstreak, 'Kills': kills, 'Comm': comm},
                           sel=UID)
    except:
        # Print Error Message
        error = 'Python: Error parsing search Info\n'
        error = error + '%s%s\n' % (sys.exc_info()[0], sys.exc_info()[1])
        ConsolePrint(error)


def GUI_stats_clan_show(Clan_ID=-1, UID=-1):
    global thread_miniclan
    if not (thread_miniclan == None) and thread_miniclan.isAlive():
        return
    thread_miniclan = createThread("import cl_clans; cl_clans.GUI_stats_clan_show_thread(%s, %s)" % (Clan_ID, UID))


def GUI_stats_clan_show_thread(Clan_ID, UID):
    ''' show mini clan info '''
    try:
        global join_CID

        # clear data of old clan info, so it is empty while downloading data
        CommandBuffer('select mini_clan_panel:banner; param url ""')
        CommandBuffer('o_scrollbuffer clear %(Panel)s; o_scrollbuffer selectable %(Panel)s 0' \
                      % {'Panel': 'claninfo_mini_sb'})
        CommandBuffer('o_scrollbuffer clear %(Panel)s; o_scrollbuffer selectable %(Panel)s 0' \
                      % {'Panel': 'members_mini_sb'})
        gui.Focus('mini_clan_panel');

        ClanID = int(float(Clan_ID))
        # if no ClanID was given, find it out using the UID
        if ClanID == -1:
            info = Client_GetInfo(int(UID))
            if not ('Error' in info):
                ClanID = info['ClanID']
        # if player not in clan, don't continue
        if ClanID == 0:
            print_line(scroll='claninfo_mini_sb', line=' ^900This player is currently not in a clan,')
            return

        # set the clan the user possibly wants to join
        join_CID = Clan_ID

        # get the neccesary data
        clan_info = Clan_GetInfo(ClanID)

        # show the clan banner
        CommandBuffer(
            'select mini_clan_panel:banner; param url "%s%i.jpg"' % (CvarGetString('clan_banner_url'), ClanID))
        # claninfo_mini buffer
        GUI_show_clan_info('claninfo_mini_sb', ClanID, clan_info)
        # members_mini buffer
        GUI_show_members_info('members_mini_sb', ClanID, clan_info)

    except:
        # Print Error Message
        error = "Python: Stats Clan Show\n"
        error = error + "%s%s\n" % (sys.exc_info()[0], sys.exc_info()[1])
        ConsolePrint(error)


def progress(percentage, color=0):
    ''' Show Progress Bar '''
    try:
        l_e = "^icon ../clanpanel/left_empty^"
        l_h = "^icon ../clanpanel/left_half^"
        l_f_b = "^icon ../clanpanel/left_full_start^"
        l_f_a = "^icon ../clanpanel/left_full_stop^"
        m_e = "^icon ../clanpanel/middle_empty^"
        m_h = "^icon ../clanpanel/middle_half^"
        m_f_b = "^icon ../clanpanel/middle_full_start^"
        m_f_a = "^icon ../clanpanel/middle_full_stop^"
        r_e = "^icon ../clanpanel/right_empty^"
        r_h = "^icon ../clanpanel/right_half^"
        r_f = "^icon ../clanpanel/right_full^"

        default_color = '^b'

        if percentage > 100:
            perc = 100
        elif percentage < 0:
            perc = 0

        perc = (percentage / 10) * 10;

        if perc == 0:
            clr = default_color if color == 0 else '^901'
            return l_e + m_e + m_e + m_e + r_e
        elif perc == 10:
            clr = default_color if color == 0 else '^811'
            return clr + l_h + m_e + m_e + m_e + r_e
        elif perc == 20:
            clr = default_color if color == 0 else '^721'
            return clr + l_f_a + m_e + m_e + m_e + r_e
        elif perc == 30:
            clr = default_color if color == 0 else '^631'
            return clr + l_f_b + m_h + m_e + m_e + r_e
        elif perc == 40:
            clr = default_color if color == 0 else '^541'
            return clr + l_f_b + m_f_a + m_e + m_e + r_e
        elif perc == 50:
            clr = default_color if color == 0 else '^451'
            return clr + l_f_b + m_f_b + m_h + m_e + r_e
        elif perc == 60:
            clr = default_color if color == 0 else '^361'
            return clr + l_f_b + m_f_b + m_f_a + m_e + r_e
        elif perc == 70:
            clr = default_color if color == 0 else '^271'
            return clr + l_f_b + m_f_b + m_f_b + m_h + r_e
        elif perc == 80:
            clr = default_color if color == 0 else '^181'
            return clr + l_f_b + m_f_b + m_f_b + m_f_a + r_e
        elif perc == 90:
            clr = default_color if color == 0 else '^091'
            return clr + l_f_b + m_f_b + m_f_b + m_f_b + r_h
        else:
            clr = default_color if color == 0 else '^091'
            return clr + l_f_b + m_f_b + m_f_b + m_f_b + r_f

    except:
        # Print Error Message
        error = "Python: Error showing Progress Bar\n"
        error = error + "%s%s\n" % (sys.exc_info()[0], sys.exc_info()[1])
        ConsolePrint(error)


def print_info(info, func=None, *textbuffers):
    ''' Print returned info/error from server '''
    try:
        type = 'Error' if ('Error' in info) else 'Info'
        for textbuffer in textbuffers:
            CommandExec('textbuffer clear %(Textbuffer)s; \
            textbuffer print %(Textbuffer)s "%(Color)s%(Text)s"' \
                        % {"Textbuffer": textbuffer, "Color": '^900' if type == 'Error' else '^g',
                           "Text": info[type]})
        if type == 'Info' and func is not None:
            func()
    except:
        ConsolePrint('Error printing info/error returned by server\n')


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


def print_text(name, text, buffered=1):
    lines = text.splitlines()
    for line in lines:
        print_line(name, line, "", "", buffered)


def escape(text):
    ''' don't use a $/# sign within expressions'''
    return text.replace("$", "S").replace("#", "")


def legacy_createclan():
    # Display some help
    ConsolePrint('(deprecated) Please use "clanCreate <abbrev> <name>" instead.\n')


def legacy_leaveclan():
    # Display some help
    ConsolePrint('(deprecated) Please use "clanLeave" instead.\n')


def legacy_newicon():
    # Display some help
    ConsolePrint('(deprecated) Please use "clanIcon <filename>" instead.\n')


def legacy_invite():
    # Display some help
    ConsolePrint('(deprecated) Please use "clanInvite <UID>" instead.\n')
    ConsolePrint('Note: To get the UID of another Player, use "showUID <name>".\n')


def legacy_joinclan():
    # Display some help
    ConsolePrint('(deprecated) Please use "clanAcceptInvitation <ClanID>" instead.\n')
    ConsolePrint('Note: To see your list of invitations, use "clanListInvitations".\n')


def legacy_kickfromclan():
    # Display some help
    ConsolePrint('(deprecated) Please use "clanKick <UID>" instead.\n')
    ConsolePrint('Note: To see the UIDs of clan members, use "clanMembers".\n')


def legacy_makeclanadmin():
    # Display some help
    ConsolePrint('(deprecated) Please use "clanPromoteAdmin <UID>" instead.\n')
    ConsolePrint('Note: To see the UIDs of clan members, use "clanMembers".\n')


def legacy_transfersuperadmin():
    # Display some help
    ConsolePrint('(deprecated) Please use "clanTransferFounder <UID>" instead.\n')
    ConsolePrint('Note: To see the UIDs of clan members, use "clanMembers".\n')


def legacy_userkickfromclan():
    # Display some help
    ConsolePrint('(deprecated) Please use "clanKick <UID>" instead.\n')
    ConsolePrint('Note: To see the UIDs of clan members, use "clanMembers".\n')


def legacy_usermakeclanadmin():
    # Display some help
    ConsolePrint('(deprecated) Please use "clanPromoteAdmin <UID>" instead.\n')
    ConsolePrint('Note: To see the UIDs of clan members, use "clanMembers".\n')


def legacy_usertransfersuperadmin():
    # Display some help
    ConsolePrint('(deprecated) Please use "clanTransferFounder <UID>" instead.\n')
    ConsolePrint('Note: To see the UIDs of clan members, use "clanMembers".\n')
