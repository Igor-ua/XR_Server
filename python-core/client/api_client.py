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


class Player:
        def __init__(self):
                self.uid = 3
                self.name = "Mike"
                self.ac = AccuracyStats()
                pass

        def json_repr(self):
                return dict(uid=self.uid, lastUsedName=self.name, accuracyStats=self.ac)

        def __str__(self):
                return "Player: [UID: %s], [NAME: %s]" % (self.uid, self.name)


class AccuracyStats:
        def __init__(self):
                self.uid = 0
                self.desc = 'Coil Rifle'
                self.shots = 0
                self.hits = 0
                self.frags = 0
                self.accuracy_percent = 0
                self.timestamp = 0

        def json_repr(self):
                return dict(uid=self.uid, desc=self.desc, lastShots=self.shots, lastFrags=self.frags,
                            lastHits=self.hits)

        def __str__(self):
                return "Coil Rifle: [UID: %s], [ACCURACY: %s], [SHOTS: %s], [FRAGS: %s], [HITS: %s]" % (
                        self.uid, self.accuracy_percent, self.shots, self.frags, self.hits)


player = Player()


p1 = Player()
p2 = Player()
p3 = Player()
p3.uid = 4

players = list()
players.append(p1)
players.append(p2)
players.append(p3)


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
