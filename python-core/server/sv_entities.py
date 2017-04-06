import copy


# Don't save players with UID = 0 (0 is for unauthorized clients)
class Player(object):

    # Robot icon
    default_clan_id = 86846
    default_clan_tag = '^gBOT'

    def __init__(self, uid):
        self.uid = uid
        self.clan_id = self.default_clan_id
        self.clan_tag = self.default_clan_tag
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
        self.first_frag = 0
        # 0 means no award; 1 - got award
        self.last_frag = 0
        self.jumps = 0

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
        template = {"uid": 0, "clan_id": Player.default_clan_id, "name": "", "value": 0, "full_nick": "",
                    "clan_tag": Player.default_clan_tag}
        # most kills - deaths
        self.mvp = copy.copy(template)
        self.mvp["award_text"] = '%s (kills - deaths)'
        # most kills
        self.sadist = copy.copy(template)
        self.sadist["award_text"] = '%s Kills'
        # most kills in a row
        self.survivor = copy.copy(template)
        self.survivor["award_text"] = '%s Kills in a row'
        # most deaths
        self.ripper = copy.copy(template)
        self.ripper["award_text"] = '%s Deaths'
        # most npcs killed
        self.phoe = copy.copy(template)
        self.phoe["award_text"] = '%s Npc kills'
        # most accurate
        self.aimbot = copy.copy(template)
        self.aimbot["award_text"] = '%s%% Accuracy'
        # first frag
        self.first_frag = copy.copy(template)
        self.first_frag["award_text"] = 'First kill'
        # last frag that made your team win
        self.last_frag = copy.copy(template)
        self.last_frag["award_text"] = 'Last kill'
        # 0 deaths
        self.camper = copy.copy(template)
        self.camper["award_text"] = '%s Deaths'
        # fpm (frags per minute): game time / frags
        self.fpm = copy.copy(template)
        self.fpm["award_text"] = '%s Kills per minute'
        # bunny
        self.bunny = copy.copy(template)
        self.bunny["award_text"] = '%s Jumps'

    def update_awards_text(self):
        default_value = 0
        self.mvp["award_text"] %= self.mvp["value"] if self.mvp["value"] > 0 else default_value
        self.sadist["award_text"] %= self.sadist["value"] if self.sadist["value"] > 0 else default_value
        self.survivor["award_text"] %= self.survivor["value"] if self.survivor["value"] > 0 else default_value
        self.ripper["award_text"] %= self.ripper["value"] if self.ripper["value"] > 0 else default_value
        self.phoe["award_text"] %= self.phoe["value"] if self.phoe["value"] > 0 else default_value
        self.aimbot["award_text"] %= self.aimbot["value"] if self.aimbot["value"] > 0 else default_value
        self.camper["award_text"] %= self.camper["value"] if self.camper["value"] > 0 else default_value
        self.fpm["award_text"] %= self.fpm["value"] if self.fpm["value"] > 0 else default_value
        self.bunny["award_text"] %= self.bunny["value"] if self.bunny["value"] > 0 else default_value

    # Hardcoded structure
    def get_transmit_value(self):
        self.update_awards_text()
        delimiter = ','
        result = \
            str(self.mvp["award_text"]) + delimiter + str(self.mvp["full_nick"]) + delimiter + \
            str(self.sadist["award_text"]) + delimiter + str(self.sadist["full_nick"]) + delimiter + \
            str(self.survivor["award_text"]) + delimiter + str(self.survivor["full_nick"]) + delimiter + \
            str(self.ripper["award_text"]) + delimiter + str(self.ripper["full_nick"]) + delimiter + \
            str(self.phoe["award_text"]) + delimiter + str(self.phoe["full_nick"]) + delimiter + \
            str(self.aimbot["award_text"]) + delimiter + str(self.aimbot["full_nick"]) + delimiter + \
            str(self.first_frag["award_text"]) + delimiter + str(self.first_frag["full_nick"]) + delimiter + \
            str(self.last_frag["award_text"]) + delimiter + str(self.last_frag["full_nick"]) + delimiter + \
            str(self.camper["award_text"]) + delimiter + str(self.camper["full_nick"]) + delimiter + \
            str(self.fpm["award_text"]) + delimiter + str(self.fpm["full_nick"]) + delimiter + \
            str(self.bunny["award_text"]) + delimiter + str(self.bunny["full_nick"]) + delimiter
        return result


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
