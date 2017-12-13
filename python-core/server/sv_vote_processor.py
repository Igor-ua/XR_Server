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

# 347693: Rin
BANNED_UIDS = {347693}


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
