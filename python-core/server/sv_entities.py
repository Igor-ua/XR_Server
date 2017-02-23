import copy


# Don't save players with UID = 0 (0 is for unauthorized clients)
class Player(object):

    # Robot icon
    default_clan_id = 86846

    def __init__(self, uid):
        self.uid = uid
        self.clan_id = self.default_clan_id
        self.last_used_name = ""
        self.accuracy_stats = AccuracyStats(self.uid)
        self.awards = Awards(self.uid)
        # These attributes should not be sent through the json
        self.kills = 0
        self.deaths = 0
        self.killstreak = 0
        self.npc_killed = 0
        self.mvp = 0
        # frags per minute
        self.fpm = 0
        # 0 means no award; 1 - got award
        self.fist_frag = 0
        # 0 means no award; 1 - got award
        self.last_frag = 0

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
        template = {"uid": 0, "clan_id": Player.default_clan_id, "name": "", "value": 0}
        # most kills - deaths
        self.mvp = copy.copy(template)
        # most kills
        self.sadist = copy.copy(template)
        # most kills in a row
        self.survivor = copy.copy(template)
        # most deaths
        self.ripper = copy.copy(template)
        # most npcs killed
        self.phoe = copy.copy(template)
        # most accurate
        self.aimbot = copy.copy(template)
        # first frag
        self.first_frag = copy.copy(template)
        # last frag that made your team win
        self.last_frag = copy.copy(template)
        # 0 deaths
        self.camper = copy.copy(template)
        # fpm (frags per minute): game time / frags
        self.fpm = copy.copy(template)
        # bunny
        self.bunny = copy.copy(template)

    # Hardcoded structure
    def get_transmit_value(self):
        delimiter = ','
        return \
            str(self.mvp["uid"]) + delimiter + str(self.mvp["clan_id"]) + delimiter + \
            self.mvp["name"] + delimiter + str(self.mvp["value"]) + delimiter + \
            str(self.sadist["uid"]) + delimiter + str(self.sadist["clan_id"]) + delimiter + \
            self.sadist["name"] + delimiter + str(self.sadist["value"]) + delimiter + \
            str(self.survivor["uid"]) + delimiter + str(self.survivor["clan_id"]) + delimiter + \
            self.survivor["name"] + delimiter + str(self.survivor["value"]) + delimiter + \
            str(self.ripper["uid"]) + delimiter + str(self.ripper["clan_id"]) + delimiter + \
            self.ripper["name"] + delimiter + str(self.ripper["value"]) + delimiter + \
            str(self.phoe["uid"]) + delimiter + str(self.phoe["clan_id"]) + delimiter + \
            self.phoe["name"] + delimiter + str(self.phoe["value"]) + delimiter + \
            str(self.aimbot["uid"]) + delimiter + str(self.aimbot["clan_id"]) + delimiter + \
            self.aimbot["name"] + delimiter + str(self.aimbot["value"]) + delimiter + \
            str(self.first_frag["uid"]) + delimiter + str(self.first_frag["clan_id"]) + delimiter + \
            self.first_frag["name"] + delimiter + str(self.first_frag["value"]) + delimiter + \
            str(self.last_frag["uid"]) + delimiter + str(self.last_frag["clan_id"]) + delimiter + \
            self.last_frag["name"] + delimiter + str(self.last_frag["value"]) + delimiter + \
            str(self.camper["uid"]) + delimiter + str(self.camper["clan_id"]) + delimiter + \
            self.camper["name"] + delimiter + str(self.camper["value"]) + delimiter + \
            str(self.fpm["uid"]) + delimiter + str(self.fpm["clan_id"]) + delimiter + \
            self.fpm["name"] + delimiter + str(self.fpm["value"]) + delimiter + \
            str(self.bunny["uid"]) + delimiter + str(self.bunny["clan_id"]) + delimiter + \
            self.bunny["name"] + delimiter + str(self.bunny["value"]) + delimiter


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


class MapStats(object):
    def __init__(self):
        self.map_name = 'default_map_name'
        self.red_score = 0
        self.blue_score = 0
        self.winner = 'draw'

    def json_repr(self):
        return dict(mapName=self.map_name, redScore=self.red_score, blueScore=self.blue_score, winner=self.winner)

    def __str__(self):
        return "MapStats: [MAP_NAME: %s], [RED: %s], [BLUE: %s], [WINNER: %s]" % (self.map_name, self.red_score,
                                                                                  self.blue_score, self.winner)
