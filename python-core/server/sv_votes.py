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

# Custom Vote Vars
global currentVote
global currentClient


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

    core.ConsolePrint('Python: callcustomvote\n') # debug
    core.ConsolePrint('clientIndex: %i\n' % clientIndex) # debug
    core.ConsolePrint('voteType: %s\n' % voteType) # debug
    core.ConsolePrint('voteInfo: %s\n' % voteInfo) # debug
    
    if voteType == 'NULL':
        server.Notify(clientIndex, 'Custom Vote Explanation')
        return -1 # doesn't count as an invalid vote
    
    # Reject vote by default
    answer = 0

    try:
        if voteType == 'test':
            answer = 1
            core.CvarSetString('sv_customVoteName', 'Testing Vote') # Custom: + own description
            core.CvarSetValue('sv_customVotePassPercent', 0.90) # float
            core.CvarSetValue('sv_customVoteAffectedIndex', -1) # -1 = none
            core.CvarSetValue('sv_customVoteMalus', 0) # defines if affected can, or has to, accept
            core.CvarSetValue('sv_customVoteVotableBy', 1) # 1 = TEAM
        else:
            core.ConsolePrint('Python: callcustomvote invalid: %i / %s / %s\n' % (clientIndex, voteType, voteInfo)) # debug
    except:
        core.ConsolePrint('Python: callcustomvote failed\n')
        sv_custom_utils.simple_exception_info()
        pass
    
    currentVote = voteType
    currentClient = clientIndex
    
    return answer


def passcustomvote(yes, no):

    core.ConsolePrint('Python: passcustomvote: %i vs %i\n' % (yes, no)) # debug
    # Accept pass by default
    answer = 1

    try:    
        # Do your thing
        pass
    
    except:
        sv_custom_utils.simple_exception_info()
        pass
        
    return answer
