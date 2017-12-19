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

CUSTOM_VOTES = ['camper', 'outcome']
custom_answer = -1

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
    core.ConsolePrint('[DEBUG] Custom vote: %i / %s / %s\n' % (clientIndex, voteType, voteInfo))
    clearCustomVoteCvars()

    if voteType not in CUSTOM_VOTES:
        server.Notify(clientIndex, 'Example: /callvote custom <voteType> <voteInfo>')
        return -1 # doesn't count as an invalid vote

    # Reject vote by default; Client gets a message: "Invalid custom vote."
    global custom_answer
    custom_answer = 0

    try:
        camper(clientIndex, voteType, voteInfo)
        outcome(clientIndex, voteType, voteInfo)
    except:
        sv_custom_utils.simple_exception_info()

    currentVote = voteType
    currentClient = clientIndex

    core.ConsolePrint('[DEBUG] Custom vote answere: [%s]\n' % custom_answer)
    return custom_answer


def camper(clientIndex, voteType, voteInfo):
    if voteType == 'camper':
        # Invalid custom vote (buil-in message)
        if voteInfo == '':
            return 0

        global custom_answer
        affectedIndex = sv_utils.getIndexFromName(str(voteInfo))
        if affectedIndex is None:
            server.Notify(clientIndex, '%s is not found' % voteInfo)
            custom_answer = -1
        else:
            custom_answer = 1
            set_custom_values('Ban siege for %s' % voteInfo, 'camper', 0.80, affectedIndex, 0, 1)


def outcome(clientIndex, voteType, voteInfo):
    if voteType == 'outcome':
        global custom_answer
        affectedIndex = sv_utils.getIndexFromName(str(voteInfo))
        custom_answer = 1
        # Block draw/concede votes for 5 min.
        # No end-game votes
        set_custom_values('Block draws for 5 min', 'outcome', 0.70, affectedIndex, 0, 0)


def passcustomvote(yes, no):
    core.ConsolePrint('[INFO] Custom vote passed: %i vs %i\n' % (yes, no))
    # Accept pass by default
    answer = 1
    voteType = core.CvarGetString('sv_customVoteType')
    try:
        if voteType == 'camper':
            guid = int(core.CvarGetValue('sv_customVoteAffectedIndex'))
            sv_respawn_handler.ban_siege_camper(guid)
        if voteType == 'outcome':
            sv_vote_processor.outcome_restricts()
    except:
        sv_custom_utils.simple_exception_info()
    return answer


def clearCustomVoteCvars():
    global custom_answer
    global currentVote
    global currentClient
    currentVote = ''
    currentClient = -1
    set_custom_values('', '', 1.00, -1, 1, 0)
    custom_answer = -1


def set_custom_values(voteName, voteType, passPercent, affectedIndex, malus, votableBy):
    core.CvarSetString('sv_customVoteName', voteName)                   # Custom: + own description
    core.CvarSetString('sv_customVoteType', voteType)                   # Custom vote type
    core.CvarSetValue('sv_customVotePassPercent', passPercent)          # float
    core.CvarSetValue('sv_customVoteAffectedIndex', affectedIndex)      # -1 = none
    core.CvarSetValue('sv_customVoteMalus', malus)                      # defines if affected can, or has to, accept; 1 - has NOT to accept; 0 - HAS to accept. 1 - has NOT
    # if 1 - "Player has accepted the vote. 0 - vote goes on. Should be 0"
    core.CvarSetValue('sv_customVoteVotableBy', votableBy)              # 1 = TEAM
