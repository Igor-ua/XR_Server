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


# r = requests.post(url, json=data, headers=headers)
r = requests.post(url, data=json.dumps(data))

print r.text