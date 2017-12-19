# ---------------------------------------------------------------------------
#           Name: sv_vote_processor.py
#    Description: different vote handlers
# ---------------------------------------------------------------------------


# Savage API
import core
import server
import datetime

# External modules
import sv_maps
import time

# 347693: Rin
BANNED_UIDS = {347693}

outcomeIsOn = False

# Sec:
OUTCOME_PERIOD_MIN = 5 * 1000 * 60
outcome_start_millis = 0

def process_vote(guid, vote_type, vote_info):
    uid = int(server.GetClientInfo(guid, INFO_UID))
    name = server.GetClientInfo(guid, INFO_NAME)
    answer = check_rights_for_vote(uid, name, vote_type, vote_info)

    if vote_type == 'world':
        answer = process_world(guid, vote_type, vote_info, answer)

    if vote_type == 'nextmap':
        answer = process_nextmap(guid, vote_type, vote_info, answer)

    if vote_type == 'msg':
        answer = process_msg(guid, vote_type, vote_info, answer)

    if vote_type == 'draw':
        answer = process_draw(guid, vote_type, vote_info, answer)

    # if vote_type == 'concede':
    #     answer = process_concede(guid, vote_type, vote_info, answer)

    return answer

def check_rights_for_vote(uid, name, vote_type, vote_info):
    # Accept vote by default
    answer = 1
    if uid in BANNED_UIDS:
        answer = 0
        core.ConsolePrint('[BLOCKED] VOTE: [%s@%s] [%s] [%s]\n' % (uid, name, vote_type, vote_info))
    else:
        core.ConsolePrint('[ALLOWED] VOTE: [%s@%s] [%s] [%s]\n' % (uid, name, vote_type, vote_info))
    return answer


def process_world(guid, vote_type, vote_info, answer):
    if server.GetGameInfo(GAME_STATE) == 3:
        answer = 0
        # Notify client
        server.Notify(guid, '^900[World] ^yis ^900disabled ^ywhen ^ythe ^ygame ^yis ^yin ^yprogress.')
        return answer
    answer = sv_maps.callvote(guid, vote_info)
    return answer


def process_msg(guid, vote_type, vote_info, answer):
    return answer


def process_nextmap(guid, vote_type, vote_info, answer):
    if server.GetGameInfo(GAME_STATE) == 3:
        answer = 0
        # Notify client
        server.Notify(guid, '^900[Nextmap] ^yis ^900disabled ^ywhen ^ythe ^ygame ^yis ^yin ^yprogress.')
        return answer
    return answer


def process_draw(guid, vote_type, vote_info, answer):
    if server.GetGameInfo(GAME_STATE) == 3 and not is_outcome_passed():
        answer = 0
        # Notify client
        server.Notify(guid, 'Draw votes were blocked for 5 minutes')
    return answer


def process_concede(guid, vote_type, vote_info, answer):
    if server.GetGameInfo(GAME_STATE) == 3 and not is_outcome_passed():
        answer = 0
        # Notify client
        server.Notify(guid, 'Concede votes were blocked for 5 minutes')
    return answer


def outcome_restricts():
    global outcomeIsOn
    global outcome_start_millis
    outcomeIsOn = True
    outcome_start_millis = int(round(time.time() * 1000))


def is_outcome_passed():
    global outcomeIsOn
    current_time_millis = int(round(time.time() * 1000))
    if outcomeIsOn is True:
        if current_time_millis > outcome_start_millis + OUTCOME_PERIOD_MIN:
            outcomeIsOn = False
        else:
            return False
    return True
