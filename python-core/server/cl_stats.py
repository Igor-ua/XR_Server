# ---------------------------------------------------------------------------
#           Name: cl_stats.py
#         Author: Anthony Beaucamp (aka Mohican)
#  Last Modified: 27/11/2011
#    Description: Fetch and display Player Statistics
# ---------------------------------------------------------------------------

# Savage API
from core import *
from cl_utils import *


# -------------------------------
def init():
    # Init some cvars
    CommandExec('createvar _rank_mode kills')
    CommandExec('createvar _rank_label kills')

    # Register various Console Commands
    RegisterCmd('addBuddy', 'cl_stats', 'add_buddy')
    RegisterCmd('remBuddy', 'cl_stats', 'rem_buddy')
    RegisterCmd('changePortrait', 'cl_stats', 'change_portrait')
    RegisterCmd("statsPrint", "cl_stats", "stats_print")

    RegisterCmd("GUI_statsShow", "cl_stats", "GUI_stats_show")
    RegisterCmd("GUI_statsProfile", "cl_stats", "GUI_stats_profile")
    RegisterCmd("GUI_statsRanking", "cl_stats", "GUI_stats_ranking")
    RegisterCmd("GUI_statsBuddies", "cl_stats", "GUI_stats_buddies")
    RegisterCmd('GUI_statsManage', 'cl_stats', 'GUI_stats_manage')


# -------------------------------
def add_buddy(UID):
    # Process this command with a Thread!
    createThread('import cl_stats; cl_stats.add_buddy_thread(%i)' % int(float(UID)))


def add_buddy_thread(UID):
    info = Client_Manage({'addBuddy': UID})
    ConsolePrint('%s\n' % info)


def rem_buddy(UID):
    # Don't use a Thread for this one...
    info = Client_Manage({'remBuddy': int(float(UID))})
    ConsolePrint('%s\n' % info)


def change_portrait(filename):
    # Don't use a Thread for this one...
    info = Client_Manage({'changePortrait': str(filename)})
    CommandBuffer('flushgraphicurl "%s%i.jpg"' % (CvarGetString('user_portrait_url'), getLoginInfo('UID')))
    CommandBuffer('cachegraphicurl "%s%i.jpg"' % (CvarGetString('user_portrait_url'), getLoginInfo('UID')))
    ConsolePrint('%s\n' % info)


# -------------------------------
def stats_print(UID):
    # Process this command with a Thread!
    createThread('import cl_stats; cl_stats.stats_print_thread(%i)' % int(float(UID)))


def stats_print_thread(UID):
    # Safety Check
    if UID == 0:
        message = 'This player is not using XR, cannot display statistics.\n'
        ConsolePrint(message)
        return

    # Just print Stats in Console
    info = Client_GetStatsLong(UID)
    ConsolePrint('%s\n' % str(info))


# -------------------------------
def GUI_stats_show(UID):
    # Safety Check
    UID = int(float(UID))
    if UID == 0:
        message = 'Player is not Authenticated, cannot display statistics.\n'
        CommandBuffer(
            'show info_panel; textbuffer clear info_panel:info_explanation; textbuffer print info_panel:info_explanation "%s"' % message)
        return

    # Show Panel
    CommandBuffer('show userinfo_panel; panel focus userinfo_panel')

    # Update Portrait and Buttons
    CvarSetValue('_stats_UID', UID)
    CommandBuffer('select userinfo_panel:portrait; param url "%s%i.jpg"' % (CvarGetString('user_portrait_url'), UID))
    CommandBuffer('select userinfo_panel:profile; param command "GUI_statsProfile %i"' % UID)
    CommandBuffer('select userinfo_panel:ranking; param command "GUI_statsRanking %i"' % UID)
    if UID == getLoginInfo('UID'):
        CommandBuffer('hide userinfo_panel:addbuddy; show userinfo_panel:manage')
    else:
        CommandBuffer('show userinfo_panel:addbuddy; hide userinfo_panel:manage')
        CommandBuffer('select userinfo_panel:addbuddy; param command "addBuddy %i"' % UID)

        # Process data with 2 threads!
    createThread('import cl_stats; cl_stats.stats_profile_thread(%i)' % UID)
    createThread('import cl_stats; cl_stats.stats_buddies_thread(%i)' % UID)


def GUI_stats_buddies(UID):
    # Process this command with 1 thread!
    createThread('import cl_stats; cl_stats.stats_buddies_thread(%i)' % int(float(UID)))


def GUI_stats_ranking(UID):
    # Process this command with 1 thread!
    createThread('import cl_stats; cl_stats.stats_ranking_thread(%i)' % int(float(UID)))


def GUI_stats_profile(UID):
    # Process this command with 1 thread!
    createThread('import cl_stats; cl_stats.stats_profile_thread(%i)' % int(float(UID)))


def GUI_stats_manage():
    # Get GUI information
    portrait_filename = CvarGetString('portrait_filename')

    # Update Portrait?
    if portrait_filename != '':
        change_portrait(portrait_filename)


        # -------------------------------


def stats_buddies_thread(UID):
    # Clear ScrollBuffer
    CommandBuffer('o_scrollbuffer clear %(Panel)s; o_scrollbuffer selectable %(Panel)s 0' % {'Panel': 'buddies_sb'})

    # Safety Check
    if UID == 0:
        return

    # Fetch information from AUTH
    buddies = Client_GetBuddies(UID)

    # Print into ScrollBuffer
    for i in range(len(buddies['listUID'])):
        print_line(scroll='buddies_sb', line='%(Abbrev)s^w^clan %(ClanID)s^%(Name)s^col^' % \
                                             {'Abbrev': buddies['listClanAbbrev'][i],
                                              'ClanID': str(buddies['listClanID'][i]),
                                              'Name': buddies['listName'][i]}, sel=str(buddies['listUID'][i]))


def stats_ranking_thread(UID):
    # Update Buttons
    CommandBuffer('select userinfo_panel:profile; param text_color 1 1 1')
    CommandBuffer('select userinfo_panel:ranking; param text_color 1 .8 0')
    CommandBuffer('show userinfo_panel:rankmode_menu')

    # Reset Table
    for n in xrange(21):
        update_cell(0, n, "")
        update_cell(1, n, "")
    update_cell(1, 0, "Please Wait")

    # Safety Check
    if UID == 0:
        return

        # Fetch ranking from AUTH
    ranks = Client_GetRanking(UID, CvarGetString('_rank_mode'))
    if 'Error' in ranks:
        update_cell(1, 0, ranks['Error'])
        return

    # Populate Table
    row = 0
    update_cell(0, row, "^980Rank")
    update_cell(1, row, "^980Achievement")
    row += 2

    for index in range(len(ranks['listUID'])):
        if index > 14:
            update_cell(0, row, "^w...")
            update_cell(1, row, "^w...")
            row += 1

        if ranks["listUID"][index] == UID:
            update_cell(0, row, "^980[%i]^w - %s^w^clan %i^%s" % (
            ranks["listRank"][index], ranks["listClanAbbrev"][index], ranks["listClanID"][index],
            ranks["listName"][index]))
            update_cell(1, row, "^980%i %s" % (ranks['listValue'][index], CvarGetString('_rank_label')))
        else:
            update_cell(0, row, "[%i] - %s^w^clan %i^%s" % (
            ranks["listRank"][index], ranks["listClanAbbrev"][index], ranks["listClanID"][index],
            ranks["listName"][index]))
            update_cell(1, row, "^w%i %s" % (ranks['listValue'][index], CvarGetString('_rank_label')))
        row += 1


def stats_profile_thread(UID):
    # Update Buttons
    CommandBuffer('select userinfo_panel:profile; param text_color 1 .8 0')
    CommandBuffer('select userinfo_panel:ranking; param text_color 1 1 1')
    CommandBuffer('hide userinfo_panel:rankmode_menu')

    # Define Tags
    Awards = ["homewrecker", "downsizer", "sadist", "unbreak", "hero", "capitalist", \
              "veteran", "bestminer", "teacherpet", "besthealer", "mmorpg", "reaper"]  # sacrifices

    # Reset Awards and Table
    for n in xrange(12):
        update_award(Awards[n], "")
    for n in xrange(21):
        update_cell(0, n, "")
        update_cell(1, n, "")
    update_cell(1, 0, "Please Wait")

    # Safety Check
    if UID == 0:
        return

        # Fetch stats from AUTH
    stats = Client_GetStatsLong(UID)
    if 'Error' in stats:
        update_cell(1, 0, stats['Error'])
        return

    # Populate Table
    row = 0
    try:
        # Transfer Client Info to Panel
        update_cell(1, row, stats["Username"])
        update_cell(0, row, "Username")
        row += 1

        update_cell(1, row, "%s^w^clan %i^%s" % (stats["ClanAbbrev"], stats["ClanID"], stats["NameMostUsed"]))
        update_cell(0, row, "Name Most Used")
        row += 1

        update_cell(1, row, "%s^w^clan %i^%s" % (stats["ClanAbbrev"], stats["ClanID"], stats["NameLastUsed"]))
        update_cell(0, row, "Name Last Used")
        row += 1

        update_cell(1, row, stats["LastSeen"])
        update_cell(0, row, "Last Seen")
        row += 1

        # Transfer Client Stats to Panel
        update_cell(1, row, "%i hours" % (stats["playTime"] // 3600000))
        update_cell(0, row, "Total Playtime")
        row += 1

        update_cell(1, row, "^r%i^w/^r%i^w/^r%i" % (stats["kicked"], stats["impeached"], stats["muted"]))
        update_cell(0, row, "Kicked / Impeached / Muted")
        row += 1

        if stats["lostgame"] > 0:
            ratio = float(stats["wongame"]) / float(stats["lostgame"])
        else:
            ratio = 0
        update_cell(1, row, "^g%i^w/^r%i ^w(%.2f)" % (stats["wongame"], stats["lostgame"], ratio))
        update_cell(0, row, "Game Wins / Losses")
        row += 1

        if stats["lost"] > 0:
            ratio = float(stats["won"]) / float(stats["lost"])
        else:
            ratio = 0
        update_cell(1, row, "^g%i^w/^r%i ^w(%.2f)" % (stats["won"], stats["lost"], ratio))
        update_cell(0, row, "Commander Wins / Losses")
        row += 1

        if stats["moneySpent"] > 0:
            ratio = float(stats["moneyGained"]) / float(stats["moneySpent"])
        else:
            ratio = 0
        update_cell(1, row, "^g%i^w/^r%i ^w(%.2f)" % (stats["moneyGained"], stats["moneySpent"], ratio))
        update_cell(0, row, "Money Earned / Spent")
        row += 1

        if stats["deaths"] > 0:
            ratio = float(stats["kills"]) / float(stats["deaths"])
        else:
            ratio = 0
        update_cell(1, row, "^g%i^w/^r%i ^w(%.2f)" % (stats["kills"], stats["deaths"], ratio))
        update_cell(0, row, "Player Kills / Deaths")
        row += 1

        update_cell(1, row, "%i kills" % stats["mostKillsSinceRespawn"])
        update_cell(0, row, "Longest Killstreak")
        row += 1

        update_cell(1, row, stats["npcKills"])
        update_cell(0, row, "NPCs Killed")
        row += 1

        update_cell(1, row, stats["aiUnitKills"])
        update_cell(0, row, "Workers Killed")
        row += 1

        update_cell(1, row, stats["buildingKills"])
        update_cell(0, row, "Buildings Destroyed")
        row += 1

        update_cell(1, row, stats["FlagsCaptured"])
        update_cell(0, row, "Flags Captured")
        row += 1

        update_cell(1, row, stats["usedBuffs"])
        update_cell(0, row, "Buffs Used")
        row += 1

        update_cell(1, row, stats["numJumps"])
        update_cell(0, row, "Jumps")
        row += 1

        totalXP = stats["generalXP"] + stats["commXP"] + stats["medXP"] * 10

        update_cell(1, row, "%i percent" % (100 * stats["commXP"] // totalXP))
        update_cell(0, row, "Commander XP")
        row += 1

        update_cell(1, row, "%i percent" % (100 * stats["generalXP"] // totalXP))
        update_cell(0, row, "Figther XP")
        row += 1

        update_cell(1, row, "%i percent" % (100 * stats["medXP"] * 10 // totalXP))
        update_cell(0, row, "Healer XP")

    except:
        update_cell(1, row, "No other stats available yet")

    # Always show UID at bottom
    update_cell(0, 20, "UID")
    update_cell(1, 20, "%i" % (UID))

    # Transfer Client Awards to Panel    
    for n in xrange(len(Awards)):
        update_award(Awards[n], stats[Awards[n]])


def update_cell(col, row, value):
    CommandBuffer('select userinfo_panel:col%i_row%i; param text "%s"' % (col, row, str(value)))


def update_award(name, value):
    CommandBuffer('select userinfo_panel:%s_value; param text "%s"' % (name, str(value)))
