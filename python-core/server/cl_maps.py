# ---------------------------------------------------------------------------
#           Name: cl_maps.py
#         Author: Anthony Beaucamp (aka Mohican)
#  Last Modified: 21/01/2012
#    Description: Map Rating and Commenting Functions
# ---------------------------------------------------------------------------

# Savage API
from core import *
from cl_utils import *


# -------------------------------
def init():
    # Register various Console Commands

    RegisterCmd('GUI_getMapInfo', 'cl_maps', 'GUI_getMapInfo')
    RegisterCmd('GUI_getMapReview', 'cl_maps', 'GUI_getMapReview')
    RegisterCmd('GUI_getMapRating', 'cl_maps', 'GUI_getMapRating')

    RegisterCmd('GUI_setMapReview', 'cl_maps', 'GUI_setMapReview')
    RegisterCmd('GUI_setMapRating', 'cl_maps', 'GUI_setMapRating')

    RegisterCmd('getMapRating', 'cl_maps', 'getMapRating')
    RegisterCmd('getMapReview', 'cl_maps', 'getMapReview')

    RegisterCmd('setMapRating', 'cl_maps', 'setMapRating')
    RegisterCmd('setMapReview', 'cl_maps', 'setMapReview')


# -------------------------------
def GUI_getMapInfo(Name):
    # Process this Command with a Thread!
    createThread('import cl_maps; cl_maps.GUI_getMapInfo_thread("%s")' % str(Name))


def GUI_getMapInfo_thread(Name):
    # Fetch info from Auth
    info = Map_GetInfo(Name)
    CommandBuffer('select map_stats_panel:author; param text "%s"' % info['Author'])
    CommandBuffer('select map_stats_panel:time; param text "%i min"' % (int(info['AverageTime'] / 60)))
    CommandBuffer('select map_stats_panel:play; param text "%i"' % info['PlayCount'])
    CommandBuffer('select map_stats_panel:draw; param text "%i"' % info['DrawCount'])
    CommandBuffer('select map_stats_panel:human; param text "%i"' % info['HumanCount'])
    CommandBuffer('select map_stats_panel:beast; param text "%i"' % info['BeastCount'])
    CommandBuffer('select map_stats_panel:beast; param text "%i"' % info['BeastCount'])
    CommandBuffer('select map_stats_panel:rating; param text "Rating (%i votes):"' % info['RatingCount'])

    # Show the Correct Star Icons
    if info['RatingTotal'] > 0:
        CommandBuffer('select map_stats_panel:rating1; param image /textures/icons/star-full.s2g')
    else:
        CommandBuffer('select map_stats_panel:rating1; param image /textures/icons/star-empty.s2g')

    if info['RatingTotal'] >= 1.5:
        CommandBuffer('select map_stats_panel:rating2; param image /textures/icons/star-full.s2g')
    else:
        CommandBuffer('select map_stats_panel:rating2; param image /textures/icons/star-empty.s2g')

    if info['RatingTotal'] >= 2.5:
        CommandBuffer('select map_stats_panel:rating3; param image /textures/icons/star-full.s2g')
    else:
        CommandBuffer('select map_stats_panel:rating3; param image /textures/icons/star-empty.s2g')

    if info['RatingTotal'] >= 3.5:
        CommandBuffer('select map_stats_panel:rating4; param image /textures/icons/star-full.s2g')
    else:
        CommandBuffer('select map_stats_panel:rating4; param image /textures/icons/star-empty.s2g')

    if info['RatingTotal'] >= 4.5:
        CommandBuffer('select map_stats_panel:rating5; param image /textures/icons/star-full.s2g')
    else:
        CommandBuffer('select map_stats_panel:rating5; param image /textures/icons/star-empty.s2g')

    # Print comments into scrollbuffer
    CommandBuffer('o_scrollbuffer clear map_comments_sb')
    for i in range(len(info['listUID'])):
        print_line(scroll='map_comments_sb', line='^w^clan %(ClanID)s^%(Name)s - ^w%(Message)s' % \
                                                  {'ClanID': str(info['listClanID'][i]), 'Name': info['listName'][i],
                                                   'Message': info['listMessage'][i]})


# -------------------------------
def GUI_getMapRating(Name):
    # Process this Command with a Thread!
    createThread('import cl_maps; cl_maps.GUI_getMapRating_thread("%s")' % str(Name))


def GUI_getMapRating_thread(Name):
    # Fetch info from Auth
    info = Map_GetRating(Name)
    GUI_setMapRating(info['Rating'])


def GUI_setMapRating(Rating):
    # Show the Correct Star Icons
    if int(Rating) > 0:
        CommandBuffer('select endgame_map_review:rating1; param up_image /textures/icons/star-full.s2g')
    else:
        CommandBuffer('select endgame_map_review:rating1; param up_image /textures/icons/star-empty.s2g')

    if int(Rating) > 1:
        CommandBuffer('select endgame_map_review:rating2; param up_image /textures/icons/star-full.s2g')
    else:
        CommandBuffer('select endgame_map_review:rating2; param up_image /textures/icons/star-empty.s2g')

    if int(Rating) > 2:
        CommandBuffer('select endgame_map_review:rating3; param up_image /textures/icons/star-full.s2g')
    else:
        CommandBuffer('select endgame_map_review:rating3; param up_image /textures/icons/star-empty.s2g')

    if int(Rating) > 3:
        CommandBuffer('select endgame_map_review:rating4; param up_image /textures/icons/star-full.s2g')
    else:
        CommandBuffer('select endgame_map_review:rating4; param up_image /textures/icons/star-empty.s2g')

    if int(Rating) > 4:
        CommandBuffer('select endgame_map_review:rating5; param up_image /textures/icons/star-full.s2g')
    else:
        CommandBuffer('select endgame_map_review:rating5; param up_image /textures/icons/star-empty.s2g')


# -------------------------------
def GUI_getMapReview(Name):
    # Process this command with a Thread!
    createThread('import cl_maps; cl_maps.GUI_getMapReview_thread("%s")' % str(Name))


def GUI_getMapReview_thread(Name):
    # Fetch info from Auth
    info = Map_GetReview(Name)
    CvarSetString('map_comment', str(info['Review']))


def GUI_setMapReview():
    # Process this command with a Thread!
    createThread('import cl_maps; cl_maps.GUI_setMapReview_thread()')


def GUI_setMapReview_thread():
    # Send Review Message
    Name = CvarGetString('world_name')
    Message = CvarGetString('map_comment')
    info = Map_SetReview(Name, Message)
    if 'Error' in info:
        CommandExec(
            'show info_panel; textbuffer clear info_panel:info_explanation; textbuffer print info_panel:info_explanation "%s"' %
            info['Error'])
    else:
        CommandExec(
            'show info_panel; textbuffer clear info_panel:info_explanation; textbuffer print info_panel:info_explanation "%s"' %
            info['Info'])


# -------------------------------
def getMapRating(Name):
    # Process this command with a Thread!
    createThread('import cl_maps; cl_maps.getMapRating_thread("%s")' % str(Name))


def getMapRating_thread(Name):
    # Just print Stats in Console
    info = Map_GetRating(Name)
    ConsolePrint('%s\n' % str(info))
    CvarSetValue('answer', int(info['Rating']))


# -------------------------------
def getMapReview(Name):
    # Process this command with a Thread!
    createThread('import cl_maps; cl_maps.getMapReview_thread("%s")' % str(Name))


def getMapReview_thread(Name):
    # Just print Stats in Console
    info = Map_GetReview(Name)
    ConsolePrint('%s\n' % str(info))
    CvarSetString('answer', str(info['Review']))


# -------------------------------
def setMapRating(Name, Rating):
    # Process this command with a Thread!
    createThread('import cl_maps; cl_maps.setMapRating_thread("%s",%i)' % (str(Name), int(Rating)))


def setMapRating_thread(Name, Rating):
    # Just print Stats in Console
    info = Map_SetRating(Name, Rating)
    ConsolePrint('%s\n' % str(info))


# -------------------------------
def setMapReview(Name, Message):
    # Process this command with a Thread!
    createThread('import cl_maps; cl_maps.setMapReview_thread("%s","%s")' % (str(Name), str(Message)))


def setMapReview_thread(Name, Message):
    # Just print Stats in Console
    info = Map_SetReview(Name, Message)
    ConsolePrint('%s\n' % str(info))
