# ---------------------------------------------------------------------------
#           Name: sv_maps.py
#         Author: Anthony Beaucamp (aka Mohican)
#  Last Modified: 28/01/2011
#    Description: Manager for Map Rotation and Votes
# ---------------------------------------------------------------------------

# Savage API
from core import *
from server import *

# Savage Modules
from sh_math import *

# Python Library Modules
import csv
import sys
import random
import urllib
import os

random.seed()

# Map Statistics Variables
global mapName  # List (for each map): Names of all Maps on this Server
global minPlayer  # List (for each map): Min num of Players (Range: 0~64)
global avgPlayer  # List (for each map): Best num of Players (Range: 4~128)
global maxPlayer  # List (for each map): Max num of Players (Range: 8~128)
global frequency  # List (for each map): Likelyhood of playing this Map (Range: 0.1~1.0)
global numPlayed  # List (for each map): Number of times Map has been played since Server started
global mapHistory  # List: Indexes of Maps played since Server started, in chronological order

mapFileName = 'Maplist.cfg'


# -------------------------------
def init():
    # Global Variables
    global mapName
    global minPlayer
    global avgPlayer
    global maxPlayer
    global frequency
    global numPlayed
    global mapHistory

    # Print Console Message
    ConsolePrint(' * Initializing Maps...\n')

    # Register some Console Commands
    RegisterCmd("mapsList", "sv_maps", "cmd_list")
    RegisterCmd("mapsStats", "sv_maps", "cmd_stats")
    RegisterCmd("mapsHistory", "sv_maps", "cmd_history")
    RegisterCmd("mapCheckVersion", "sv_maps", "cmd_checkversion")

    # Initialize Chronological Record
    mapHistory = []

    # Names of Maps to ignore
    mapIgnore = ["benchmark", "_undo_", "xr_tutorial_b1", "xr_tutorial_h1"]

    # Get list of Maps on this Server
    fileList = [f for f in os.listdir('world')]
    mapName = [os.path.splitext(f)[0] for f in fileList if os.path.splitext(f)[1] == '.s2z']
    mapName = [f for f in mapName if mapIgnore.count(f) == 0]

    # Initialize Statistics
    numPlayed = list(0 for n in range(0, len(mapName)))
    minPlayer = list(0 for n in range(0, len(mapName)))
    avgPlayer = list(24 for n in range(0, len(mapName)))
    maxPlayer = list(64 for n in range(0, len(mapName)))
    frequency = list(0.01 for n in range(0, len(mapName)))

    try:
        # Open Map Statistics File
        MapStats = csv.reader(open('python/sv_maps.csv', 'rb'), delimiter=',')

        # Read Row-by-Row
        row = 0
        for rowData in MapStats:
            row += 1

            # Ignore Header
            if row < 2:
                continue

            # Try to Find Map
            try:
                # Read Cell-by-Cell
                index = mapName.index(rowData[0])
                minPlayer[index] = rowData[1]
                avgPlayer[index] = rowData[2]
                maxPlayer[index] = rowData[3]
                frequency[index] = rowData[4]

                # Check there are no "sillies"
                if avgPlayer[index] > maxPlayer[index]:
                    avgPlayer[index] = maxPlayer[index]
                if frequency[index] < 0.1:
                    frequency[index] = 0.1
                if frequency[index] > 1.0:
                    frequency[index] = 1.0

            except:
                # Ignore Map
                ignoreMap = 1

    except:
        # Could not read the CSV file
        ConsolePrint("[!]   sv_maps.csv does not exist\n")

        # Make all maps equally likely
        mapTotal = len(mapName)
        for index in range(0, mapTotal):
            frequency[index] = 0.5


# -------------------------------
def savestats():
    global numPlayed
    global mapHistory

    try:
        # Get index of current Map
        name = CvarGetString('svr_world')
        index = mapName.index(name)
    except:
        # So much for trying...
        return

    # Keep record of this Map
    numPlayed[index] += 1
    mapHistory.append(index)


# Random map choice -------------------------------
def nextmap():
    mapList = []
    try:
        with open(mapFileName) as f:
            unfiltered = [c.strip() for c in f.readlines()]
        for c in unfiltered:
            if c != '' and not c.startswith('//'):
                mapList.append(c)
        current_map_name = str(CvarGetString('svr_world'))
        current_map_index = mapList.index(current_map_name)
        if current_map_index < len(mapList) - 1:
            CvarSetString('sv_nextMap', mapList[current_map_index + 1])
        else:
            CvarSetString('sv_nextMap', mapList[0])
    except:
        CvarSetString('sv_nextMap', str(CvarGetString('default_world')))


# -------------------------------
def callvote(clientIndex, mapName):
    # Need some Map Vote Logics...
    msg = "Python: Vote called for map " + mapName + "\n"
    ConsolePrint(msg)
    return 1


# -------------------------------
# Registered Console Commands
# -------------------------------
def cmd_list():
    # Some Information
    ConsolePrint("List of maps on this server:\n")

    # Display Map List in Console
    mapList = ""
    mapCounter = 0
    mapTotal = len(mapName)
    for index in range(0, mapTotal):
        # Concatenate String
        mapList = mapList + mapName[index]

        # Display in Console?
        mapCounter += 1
        if mapCounter > 5 or index == mapTotal - 1:
            mapList = mapList + "\n"
            ConsolePrint(mapList)
            mapCounter = 0
            mapList = ""
        else:
            mapList = mapList + ", "


# -------------------------------
def cmd_stats():
    # Some Information
    ConsolePrint("Statistics of maps on this server\n")
    ConsolePrint("---------------------------------\n")
    ConsolePrint("Map Name | Num Played | Min Player | Avg Player | Max Player | Frequency\n")

    # Display Map List in Console
    mapTotal = len(mapName)
    for index in range(0, mapTotal):
        msg = mapName[index] + " | " + str(numPlayed[index]) + " | " + str(minPlayer[index]) \
              + " | " + str(avgPlayer[index]) + " | " + str(maxPlayer[index]) \
              + " | " + str(frequency[index]) + "\n"
        ConsolePrint(msg)


# -------------------------------
def cmd_history():
    # Some Information
    ConsolePrint("Chronological list of maps played since server started:\n")

    # Display Map List in Console
    mapList = ""
    mapCounter = 0
    mapTotal = len(mapHistory)
    for index in range(0, mapTotal):
        # Concatenate String
        mapList = mapList + mapName[mapHistory[index]]

        # Display in Console?
        mapCounter += 1
        if mapCounter > 5 or index == mapTotal - 1:
            mapList = mapList + "\n"
            ConsolePrint(mapList)
            mapCounter = 0
            mapList = ""
        else:
            mapList = mapList + ", "


# -------------------------------
def cmd_checkversion(mapName, load=0):
    # Process this command with a Thread!
    createThread('import sv_maps; sv_maps.cmd_checkversion_thread("%s", %i)' % (mapName, int(load)))


def cmd_checkversion_thread(mapName, load=0):
    # Get size on local disk
    try:
        localSize = os.path.getsize('world/%s.s2z' % mapName)
    except:
        ConsolePrint('"%s" not found on local installation.\n' % mapName)
        localSize = 0

    # Get size on map repo
    try:
        ConsolePrint('Checking "%s" against repository (svr_mapurl)...\n' % mapName)
        online = urllib.urlopen('%s/%s.s2z' % (CvarGetString('svr_mapurl'), mapName))
        meta = online.info()
        onlineSize = int(meta.getheaders("Content-Length")[0])
    except:
        ConsolePrint('Cannot reach map repository (please check that "svr_mapurl" is set correctly).\n')
        onlineSize = 0

    # Safety check (for 404 urls)
    if onlineSize == 220:
        ConsolePrint('"%s" not found on map repository.\n' % mapName)
        onlineSize = 0

    # Compare and update if necessary
    if onlineSize == 0:
        ConsolePrint('Could not update "%s".\n' % mapName)
    elif localSize != onlineSize:
        ConsolePrint('Downloading latest version of "%s" from map repository...\n' % mapName)
        f = open('world/%s.s2z' % mapName, 'wb')
        f.write(online.read())
        f.close()
    else:
        ConsolePrint('"%s" is already up-to-date.\n' % mapName)

    # Close URL
    try:
        online.close()
    except:
        pass

    # Call this world?
    if load == 1:
        CommandBuffer('world "%s" 0' % mapName)
