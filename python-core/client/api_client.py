############################################################################################
#               This file is for testings
#               # todo delete me later
############################################################################################


import json
import requests

# data = {"uid": 4, "lastUsedName": "Mike"}

# data = {"uid": 2,
#         "lastUsedName": "Mike",
#         "accuracyStats": {"lastShots": 10, "lastHits": 5, "lastFrags": 5}
#         }

# headers = {'Content-Type': 'application/json'}
# url = 'http://localhost:8080/stats/server/save'

# headers = {'content-type': 'application/json'}
# r = requests.post(url, json=data, headers=headers)
# print r.text

# r = requests.post(url, data=json.dumps(data))
# print r.text
# print r.status_code

# import urllib
# import os
#
# svr_mapurl = "http://localhost:8080/world"
# mapName = "xr_test"
#
# online = urllib.urlopen('%s/%s.s2z' % (svr_mapurl, mapName))
# meta = online.info()
# print meta

# localSize = os.path.getsize('E:\\Code\\Projects\\XR_Server\\spring-core\\world\\xr_test.s2z')
# print localSize

# List structure:
# {"Players":
#         [
#                 {"uid" : 1, "lastUsedName" : "Mike","accuracyStats" : {"lastShots" : 10,"lastHits" : 5,"lastFrags" : 5}},
#                 {"uid" : 2, "lastUsedName" : "John","accuracyStats" : {"lastShots" : 4,"lastHits" : 1,"lastFrags" : 1}}
#         ]
# }


# Don't save players with UID = 0 (0 is for unauthorized clients)
class Player(object):
        def __init__(self, uid):
                self.uid = uid
                self.last_used_name = ""
                self.accuracy_stats = AccuracyStats(self.uid)
                self.awards = Awards(self.uid)
                # These attributes should not be sent through the json
                self.kills = 0
                self.deaths = 0
                self.killstreak = 0
                self.npc_killed = 0
                self.mvp = 0
                pass

        def json_repr(self):
                return dict(uid=self.uid, lastUsedName=self.last_used_name, accuracyStats=self.accuracy_stats,
                            awards=self.awards)

        def __str__(self):
                return "Player: [UID: %s], [NAME: %s]" % (self.uid, self.last_used_name)


class AccuracyStats(object):
        def __init__(self, uid):
                self.uid = uid
                self.desc = 'Coil Rifle'
                self.last_shots = 0
                self.last_hits = 0
                self.last_frags = 0
                self.accuracy_percent = 0
                self.timestamp = 0

        def json_repr(self):
                return dict(uid=self.uid, desc=self.desc, lastShots=self.last_shots, lastFrags=self.last_frags,
                            lastHits=self.last_hits)

        def __str__(self):
                return "Coil Rifle: [UID: %s], [ACCURACY: %s], [SHOTS: %s], [FRAGS: %s], [HITS: %s]" % (
                        self.uid, self.accuracy_percent, self.last_shots, self.last_frags, self.last_hits)


class MapAwards:
        def __init__(self):
                # most kills - deaths
                self.mvp = {"uid": 0, "name": "", "value": 0}
                # most kills
                self.sadist = {"uid": 0, "name": "", "value": 0}
                # most kills in a row
                self.survivor = {"uid": 0, "name": "", "value": 0}
                # most deaths
                self.ripper = {"uid": 0, "name": "", "value": 0}
                # most npcs killed
                self.phoe = {"uid": 0, "name": "", "value": 0}
                # most accurate
                self.aimbot = {"uid": 0, "name": "", "value": 0}


class Awards(object):
        def __init__(self, uid):
                self.uid = uid
                self.mvp = 0
                self.sadist = 0
                self.survivor = 0
                self.ripper = 0
                self.phoe = 0
                self.aimbot = 0

        def json_repr(self):
                return dict(uid=self.uid, mvp=self.mvp, sadist=self.sadist, survivor=self.survivor,
                            ripper=self.ripper, phoe=self.phoe, aimbot=self.aimbot)

        def __str__(self):
                return "Awards : [UID: %s], [AIMBOT: %s], [MVP: %s], [SADIST: %s], [SURVIVOR: %s], [RIPPER: %s], [PHOE: %s]" \
                       % (self.uid, self.aimbot, self.mvp, self.sadist, self.survivor, self.ripper, self.phoe)


p1 = Player(1)
p2 = Player(2)

p1.awards.aimbot = 1
p1.accuracy_stats.last_shots = 1
p1.accuracy_stats.last_hits = 0

p2.awards.aimbot = 0

players = list()
players.append(p1)
players.append(p2)


def obj_repr(obj):
        if hasattr(obj, 'json_repr'):
                return obj.json_repr()
        else:
                return obj.__dict__

json_players = json.dumps(players, default=obj_repr)


data = '{"Players": %s}' % json.dumps(players, default=obj_repr)
print data


url = 'http://localhost:8080/stats/server/players/put'
headers = {'content-type': 'application/json'}
r = requests.put(url, data, headers=headers)
print r.text
print r.status_code


# url = 'http://localhost:8080/stats/get/2'
# r = requests.get(url)
# data = json.loads(r.text)
# print data
# print data['awards']['accumulatedSadist']
# print data['uid']
