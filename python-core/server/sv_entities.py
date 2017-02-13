# Don't save players with UID = 0 (0 is for unauthorized clients)
class Player(object):
    def __init__(self, uid):
        self.uid = uid
        self.clan_id = 0
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
        return dict(uid=self.uid, clanId=self.clan_id, lastUsedName=self.last_used_name, accuracyStats=self.accuracy_stats,
                    awards=self.awards)

    def __str__(self):
        return "Player: [UID: %s], [CLAN_ID: %s], [NAME: %s]" % (self.uid, self.clan_id, self.last_used_name)


class AccuracyStats(object):
    def __init__(self, uid):
        self.uid = uid
        self.desc = 'Coil Rifle'

        self.last_shots = 0
        self.last_hits = 0
        self.last_frags = 0
        self.accuracy_percent = 0

        self.accumulated_shots = 0
        self.accumulated_hits = 0
        self.accumulated_frags = 0
        self.accumulated_percent = 0

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

    # Hardcoded structure
    def get_transmit_value(self):
        return \
            str(self.mvp["uid"]) + ";" + self.mvp["name"] + ";" + str(self.mvp["value"]) + ";" + \
            str(self.sadist["uid"]) + ";" + self.sadist["name"] + ";" + str(self.sadist["value"]) + ";" + \
            str(self.survivor["uid"]) + ";" + self.survivor["name"] + ";" + str(self.survivor["value"]) + ";" + \
            str(self.ripper["uid"]) + ";" + self.ripper["name"] + ";" + str(self.ripper["value"]) + ";" + \
            str(self.phoe["uid"]) + ";" + self.phoe["name"] + ";" + str(self.phoe["value"]) + ";" + \
            str(self.aimbot["uid"]) + ";" + self.aimbot["name"] + ";" + str(self.aimbot["value"]) + ";"


class Awards(object):
    def __init__(self, uid):
        self.uid = uid
        self.mvp = 0
        self.sadist = 0
        self.survivor = 0
        self.ripper = 0
        self.phoe = 0
        self.aimbot = 0

        self.accumulated_mvp = 0
        self.accumulated_sadist = 0
        self.accumulated_survivor = 0
        self.accumulated_ripper = 0
        self.accumulated_phoe = 0
        self.accumulated_aimbot = 0

    def json_repr(self):
        return dict(uid=self.uid, mvp=self.mvp, sadist=self.sadist, survivor=self.survivor,
                    ripper=self.ripper, phoe=self.phoe, aimbot=self.aimbot)

    def has_awards(self):
        return bool(self.accumulated_mvp) or bool(self.accumulated_sadist) or bool(self.accumulated_survivor) \
               or bool(self.accumulated_ripper) or bool(self.accumulated_phoe) or bool(self.accumulated_aimbot)

    def __str__(self):
        return "Awards : [UID: %s], [AIMBOT: %s], [MVP: %s], [SADIST: %s], [SURVIVOR: %s], [RIPPER: %s], [PHOE: %s]" \
               % (self.uid, self.accumulated_aimbot, self.accumulated_mvp, self.accumulated_sadist,
                  self.accumulated_survivor, self.accumulated_ripper, self.accumulated_phoe)
