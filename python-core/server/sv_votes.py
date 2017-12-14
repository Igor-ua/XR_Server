#---------------------------------------------------------------------------
#           Name: sv_votes.py
#         Author: Anthony Beaucamp (aka Mohican), Clemens Kremser
#  Last Modified: 21/10/2017
#    Description: Silverback Vote Event Entries (init, callvote, callcustomvote, passcustomvote)
#---------------------------------------------------------------------------

# Savage API
import core
import server

# Savage Modules
import sv_defs
import sv_custom_utils
import sv_vote_processor
import sv_utils
import sv_respawn_handler

# Custom Vote Vars
global currentVote
global currentClient

CUSTOM_VOTES = ['camper']

#-------------------------------
# Called directly by Silverback
#-------------------------------
def init():

    # Print Console Message
    core.ConsolePrint('Python: Initializing Server-Side Custom Votes...\n')

    try:
        # init your custom vote stuff
        pass

    except:
        # Print Error Message
        core.ConsolePrint('Python: Initialization Custom Votes FAILED!\n')
        sv_custom_utils.simple_exception_info()


# -------------------------------
# Called directly by Silverback
# -------------------------------
def callvote(guid, vote_type, vote_info):
    # Accept vote by default
    answer = 1
    try:
        answer = sv_vote_processor.process_vote(guid, vote_type, vote_info)
    except:
        sv_custom_utils.simple_exception_info()

    return answer


def callcustomvote(clientIndex, voteType, voteInfo):

    clearCustomVoteCvars()

    if voteType not in CUSTOM_VOTES:
        server.Notify(clientIndex, 'Example: /callvote custom <voteType> <voteInfo>')
        return -1 # doesn't count as an invalid vote
    if voteInfo == '':
        return 0

    # Reject vote by default; Client gets a message: "Invalid custom vote."
    answer = 0

    try:
        if voteType == 'camper':
            affectedIndex = sv_utils.getIndexFromName(str(voteInfo))
            if affectedIndex is None:
                server.Notify(clientIndex, '%s is not found' % voteInfo)
                answer = -1
            else:
                answer = 1
                core.CvarSetString('sv_customVoteName', 'Ban siege for %s' % voteInfo)
                core.CvarSetString('sv_customVoteType', 'camper')
                core.CvarSetValue('sv_customVotePassPercent', 0.80)
                core.CvarSetValue('sv_customVoteAffectedIndex', affectedIndex)
                core.CvarSetValue('sv_customVoteMalus', 1)
                core.CvarSetValue('sv_customVoteVotableBy', 0)
        else:
            core.ConsolePrint('Python: callCustomVote invalid: %i / %s / %s\n' % (clientIndex, voteType, voteInfo))
    except:
        sv_custom_utils.simple_exception_info()

    currentVote = voteType
    currentClient = clientIndex

    return answer


def clearCustomVoteCvars():
    currentVote = ''
    currentClient = -1
    core.CvarSetString('sv_customVoteName', '')              # Custom: + own description
    core.CvarSetString('sv_customVoteType', '')              # Custom vote type
    core.CvarSetValue('sv_customVotePassPercent', 1.00)      # float
    core.CvarSetValue('sv_customVoteAffectedIndex', -1)      # -1 = none
    core.CvarSetValue('sv_customVoteMalus', 1)               # defines if affected can, or has to, accept; 1 - has NOT to accept; 0 - HAS to accept. 1 - has NOT
    core.CvarSetValue('sv_customVoteVotableBy', 0)           # 1 = TEAM


def passcustomvote(yes, no):

    core.ConsolePrint('Python: passCustomVote: %i vs %i\n' % (yes, no))
    # Accept pass by default
    answer = 1

    try:
        if core.CvarGetString('sv_customVoteType') == 'camper':
            guid = int(core.CvarGetValue('sv_customVoteAffectedIndex'))
            sv_respawn_handler.ban_siege_camper(guid)
    except:
        sv_custom_utils.simple_exception_info()

    return answer
