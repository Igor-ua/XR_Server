#---------------------------------------------------------------------------
#           Name: sv_utils.py
#         Author: Anthony Beaucamp (aka Mohican), CrashDay
#  Last Modified: 31/07/2012
#    Description: Useful Routines for Finding Objects
#---------------------------------------------------------------------------

# Savage API
import server

# Savage Modules
import sv_defs

# 3rd Party Modules
from euclid import *

#-------------------------------
def getIndexFromName(name):
    for team in range(0,sv_defs.teamList_Last):
        for index in range(0,MAX_CLIENTS): 
            # Ignore inactive Client Slots and Bots
            if not server.GetClientInfo(index,INFO_ACTIVE) or sv_defs.clientList_Bot[index]:
                continue        
            
            # Check Player's Team
            if sv_defs.clientList_Team[index] != team:
                continue
           
            # Collect Information
            tempname = server.GetClientInfo(index,INFO_NAME)
            if tempname.lower().find(name.lower())!=-1:
                return index


#-------------------------------
def getIndicesFromTeam(team):
    indices=[]
    for index in range(0,MAX_CLIENTS): 
        # Ignore inactive Client Slots and Bots
        if not server.GetClientInfo(index,INFO_ACTIVE) or sv_defs.clientList_Bot[index]:
            continue        
        
        # Check Player's Team
        if str(sv_defs.clientList_Team[index]) == team:
            indices.append(str(index))
    print indices
    return indices


#-------------------------------
def getActiveIndices():
    indices=[]
    for team in range(0,sv_defs.teamList_Last):
        for index in range(0,MAX_CLIENTS): 
            # Ignore inactive Client Slots and Bots
            if not server.GetClientInfo(index,INFO_ACTIVE) or sv_defs.clientList_Bot[index]:
                continue        
            
            # Check Player's Team
            if sv_defs.clientList_Team[index] != team:
                continue
           
            # Collect Information
            indices.append(str(index))
    print indices
    return indices


#-------------------------------
def is_client(objIndex):
    
    # Test if object is any type of building
    if  sv_defs.objectList_Type[objIndex] == OBJTYPE_CLIENT:
        return 1
    else:
        return 0


#-------------------------------
def is_building(objIndex):
    
    # Test if object is any type of building
    if sv_defs.objectList_Type[objIndex] >= OBJTYPE_BASE and sv_defs.objectList_Type[objIndex] <= OBJTYPE_BUILDING:
        return 1
    else:
        return 0

        
#-------------------------------
def get_point3(objIndex):

    # Return Object position as Point3
	[x,y,z] = server.GetObjectPos(objIndex)
	return Point3(x,y,z)

    
#-------------------------------
def find_nearest_enemy(botIndex,maxDist):

    # Find nearest enemy Client
    botPos = get_point3(botIndex)
    nearestDist = maxDist
    nearestIndex = -1
    for objIndex in range(0,MAX_CLIENTS):
        # Only active clients
        if not sv_defs.objectList_Active[objIndex]:
            continue

        # Check client's team
        if sv_defs.objectList_Team[objIndex] == sv_defs.objectList_Team[botIndex]:
            continue
            
        # Check object's team (don't want no spectator)
        if sv_defs.objectList_Team[objIndex] == 0:
            continue            

        # Check client's health
        if sv_defs.objectList_Health[objIndex] <= 0:
            continue

        # Check client is not Commanding
        if objIndex == sv_defs.teamList_Commander[sv_defs.objectList_Team[objIndex]]:
            continue

        # Compare distance to current nearest
        objPos = get_point3(objIndex)
        if objPos.distance(botPos) < nearestDist:
            nearestDist = objPos.distance(botPos)
            nearestIndex = objIndex

    return nearestIndex


#-------------------------------
def find_nearest_enemy_object(botIndex,maxDist):

    # Find nearest enemy non-Client
    botPos = get_point3(botIndex)
    nearestDist = maxDist
    nearestIndex = -1
    for objIndex in range(MAX_CLIENTS,sv_defs.objectList_Last):
        # Only active Objects
        if not sv_defs.objectList_Active[objIndex]:
            continue
            
        # Check object's team
        if sv_defs.objectList_Team[objIndex] == sv_defs.objectList_Team[botIndex]:
            continue
            
        # Check object's team (don't need no neutral creeps)
        if sv_defs.objectList_Team[objIndex] == 0:
            continue

        # Check object's health
        if sv_defs.objectList_Health[objIndex] <= 0:
            continue

        # Compare distance to current nearest
        objPos = get_point3(objIndex)
        if objPos.distance(botPos) < nearestDist:
            nearestDist = objPos.distance(botPos)
            nearestIndex = objIndex

    return nearestIndex


#-------------------------------
def find_nearest_construct(botIndex,maxDist):
    
    # Find nearest ally building under construction
    botPos = get_point3(botIndex)
    nearestDist = maxDist
    nearestIndex = -1
    for objIndex in range(MAX_CLIENTS,sv_defs.objectList_Last):
        # Only active Objects
        if not sv_defs.objectList_Active[objIndex]:
            continue
            
        # Check object's team
        if not sv_defs.objectList_Team[objIndex] == sv_defs.objectList_Team[botIndex]:
            continue

        # Check object's type
        if sv_defs.objectList_Type[objIndex] < OBJTYPE_BASE or sv_defs.objectList_Type[objIndex] > OBJTYPE_BUILDING:
            continue
            
        # Check building is under contruction
        if not sv_defs.objectList_Construct[objIndex]:
            continue
            
        # Compare distance to current nearest
        objPos = get_point3(objIndex)
        if objPos.distance(botPos) < nearestDist:
            nearestDist = objPos.distance(botPos)
            nearestIndex = objIndex
    
    return nearestIndex


#-------------------------------
def find_nearest_repair(botIndex,maxDist):

    # Find nearest ally building not at full health (=needs repairing)
    botPos = get_point3(botIndex)
    nearestDist = maxDist
    nearestIndex = -1
    for objIndex in range(MAX_CLIENTS,sv_defs.objectList_Last):
        # Only active Objects
        if not sv_defs.objectList_Active[objIndex]:
            continue
            
        # Check object's team
        if not sv_defs.objectList_Team[objIndex] == sv_defs.objectList_Team[botIndex]:
            continue

        # Check object's type
        if sv_defs.objectList_Type[objIndex] < OBJTYPE_BASE or sv_defs.objectList_Type[objIndex] > OBJTYPE_BUILDING:
            continue
            
        # Check object's health
        if not sv_defs.objectList_Health[objIndex] < sv_defs.objectList_MaxHealth[objIndex]:
            continue
            
        # Compare distance to current nearest
        objPos = get_point3(objIndex)
        if objPos.distance(botPos) < nearestDist:
            nearestDist = objPos.distance(botPos)
            nearestIndex = objIndex
    
    return nearestIndex


#-------------------------------
def find_nearest_mine(botIndex,mineType):
 
    # Find nearest mine
    botPos = get_point3(botIndex)
    nearestDist = 999999999
    nearestIndex = -1
    for objIndex in range(MAX_CLIENTS,sv_defs.objectList_Last):
        # Only active Objects
        if not sv_defs.objectList_Active[objIndex]:
            continue
            
        # Check object's type (Mine!)
        if not sv_defs.objectList_Type[objIndex] == OBJTYPE_MINE:
            continue          
		
        # Check mine's resource type
        if not mineType == MINETYPE_ANY:
            if mineType == MINETYPE_GOLD:
                if not sv_defs.objectList_Name[objIndex] == 'gold_mine':
                            continue            
            elif mineType == MINETYPE_STONE:
                if not sv_defs.objectList_Name[objIndex] == 'redstone_mine':
                            continue                        
                       
        # TODO: Add check if mine has resources left?
            
        # Compare distance to current nearest
        objPos = get_point3(objIndex)
        if objPos.distance(botPos) < nearestDist:
            nearestDist = objPos.distance(botPos)
            nearestIndex = objIndex
    
    return nearestIndex


#-------------------------------
def find_nearest_critter(botIndex,maxDist,objDibber):

    # Find nearest valid goodie
    botPos = get_point3(botIndex)
    nearestDist = maxDist
    nearestIndex = -1
    for objIndex in range(MAX_CLIENTS,sv_defs.objectList_Last):
        # Only active Objects
        if not sv_defs.objectList_Active[objIndex]:
            continue

        # Is object a valid critter? (only small fry allowed!)
        if not sv_defs.objectList_Name[objIndex] == 'npc_monkit' and not sv_defs.objectList_Name[objIndex] == 'npc_oschore' and not sv_defs.objectList_Name[objIndex] == 'npc_macaque':
            continue

        # Check critter's health
        if sv_defs.objectList_Health[objIndex] <= 0:
            continue

        # Check dibs status
        if not objDibber[objIndex] == -1 and not objDibber[objIndex] == botIndex:
            continue

        # Compare distance to current nearest
        objPos = get_point3(objIndex)
        if objPos.distance(botPos) < nearestDist:
            nearestDist = objPos.distance(botPos)
            nearestIndex = objIndex

    return nearestIndex


#-------------------------------
def find_nearest_goodie(botIndex,maxDist,objDibber):

    # Find nearest valid goodie
    botPos = get_point3(botIndex)
    nearestDist = maxDist
    nearestIndex = -1
    for objIndex in range(MAX_CLIENTS,sv_defs.objectList_Last):
        # Only active Objects
        if not sv_defs.objectList_Active[objIndex]:
            continue

        # Is object a goodie?
        if not sv_defs.objectList_Name[objIndex] == 'goodiebag': #and not sv_defs.objectList_Name[objIndex] == 'ammo_box' and not sv_defs.objectList_Name[objIndex] == 'mana_stone':
            continue                                             # TODO: prevent bot from stopping, when it cant pick-up goodies like ammo

        # Check goodie's team
        if not sv_defs.objectList_Team[objIndex] == 0 and not sv_defs.objectList_Team[objIndex] == sv_defs.objectList_Team[botIndex]:
            continue

        # Check dibs status
        if not objDibber[objIndex] == -1 and not objDibber[objIndex] == botIndex:
            continue

        # Compare distance to current nearest
        objPos = get_point3(objIndex)
        if objPos.distance(botPos) < nearestDist:
            nearestDist = objPos.distance(botPos)
            nearestIndex = objIndex

    return nearestIndex


#-------------------------------
def find_best_spawnpoint(botIndex,targetPos):

    # Find nearest enemy Client
    nearestDist = 999999999
    nearestIndex = -1
    for objIndex in range(MAX_CLIENTS,sv_defs.objectList_Last):
        # Only active objects
        if not sv_defs.objectList_Active[objIndex]:
            continue

        # Is spawnpoint?
        if not sv_defs.objectList_Type[objIndex] == OBJTYPE_BASE and not sv_defs.objectList_Type[objIndex] == OBJTYPE_OUTPOST:
            continue

        # Reject spawnflags (to avoid getting stuck!)
        if sv_defs.objectList_Name[objIndex] == 'spawnflag':
            continue

        # Check spawnpoint's team
        if not sv_defs.objectList_Team[objIndex] == sv_defs.objectList_Team[botIndex]:
            continue

        # Check spawnpoint's health
        if sv_defs.objectList_Health[objIndex] <= 0:
            continue

        # Check spawnpoint is construted, 0 means constructed
        if sv_defs.objectList_Construct[objIndex] > 0:
            continue			

        # Compare distance to current nearest
        objPos = get_point3(objIndex)
        if objPos.distance(targetPos) < nearestDist:
            nearestDist = objPos.distance(targetPos)
            nearestIndex = objIndex

    return nearestIndex

