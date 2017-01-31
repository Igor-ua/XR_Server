############################################################################################
#               This file is for testings
#               # todo delete me later
############################################################################################


import json
import requests

# data = {"uid": 4, "lastUsedName": "Mike"}

data = {"uid": 2,
        "lastUsedName": "Mike",
        "accuracyStats": {"lastShots": 10, "lastHits": 5, "lastFrags": 5}
        }

headers = {'Content-Type': 'application/json'}
url = 'http://localhost:8080/stats/server/save'

# headers = {'content-type': 'application/json'}
# r = requests.post(url, json=data, headers=headers)
# print r.text

r = requests.post(url, data=json.dumps(data))

print r.text
print r.status_code

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