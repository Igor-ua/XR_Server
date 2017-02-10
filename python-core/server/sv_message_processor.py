# ---------------------------------------------------------------------------
#           Name: sv_message_processor.py
#    Description: Processing messages from sv_events
# ---------------------------------------------------------------------------

# Savage API
import core
import server

# External modules
import sv_defs
import sv_utils
import sv_stats
import sys
import time
import sv_custom_utils
import re
# Will replace all symbols from the input string that are not: 'A-Za-z-_() '
REGEXP_FOR_INPUT = '[^!^A-Z^a-z^\-^_^(^) ]'

messages = {'info', 'last', 'top'}

# Generated list of GUIDs. Contains values from 0 to 128
clients_list = []

# Default timeout interval for requests (in millis)
default_timeout_interval = long(1 * 2000)


def init():
    global clients_list
    for idx in range(0, MAX_CLIENTS):
        clients_list.append([idx, long(0)])


# Gets current timeout for the client id
# Returns time. Returns 0 if the client has not timeout
def get_client_timeout(guid):
    return long(clients_list[int(guid)][1])


# Sets a timeout for client id
def update_client_timeout(guid):
    try:
        global clients_list
        clients_list[int(guid)][1] = get_current_millis() + default_timeout_interval
    except:
        sv_custom_utils.simple_exception_info()


# Gets current time in millis
def get_current_millis():
    return int(round(time.time() * 1000))


def process_chat_message(guid, message_type, message):
    # type strings: global, team, squad, selected
    if message.startswith("!"):
        try:
            parse_request(message, guid)
        except:
            sv_custom_utils.simple_exception_info()
        return 0
    else:
        return 1


def process_private_message(sender_idx, receiver_idx, message):
    return 1


def parse_request(message, guid):
    try:
        replaced_message = re.sub(REGEXP_FOR_INPUT, '', message)
        msg_parts = replaced_message.split(' ')
        command = msg_parts[0].replace('!', '').lower()
        param = ''
        options = [int(guid), command, param]
        if len(msg_parts) > 0:
            param = msg_parts[1].lower()
        if command in messages:
            # process_request(guid, command, param)
            createThread('import sv_message_processor; sv_message_processor.process_request(%s)'
                         % options)
    except:
        sv_custom_utils.simple_exception_info()


def process_request(options):
    print('process_request: %s' % options)
    guid = options[0]
    command = options[1]
    param = options[2]
    try:
        current_millis = get_current_millis()
        uid = int(server.GetClientInfo(guid, INFO_UID))
        if get_client_timeout(guid) > current_millis:
            print('get_client_timeout(guid): %s' % get_client_timeout(guid))
            print('current_millis: %s' % current_millis)
            update_client_timeout(guid)
            notify_to_wait(guid)
        else:
            if command == 'info':
                if not param:
                    player = sv_stats.get_client_stats(uid)
                    if player.uid != 0:
                        notify_info(guid, player)
                    else:
                        nothing_was_found(guid)
                else:
                    player = sv_stats.get_client_stats_by_name(param)
                    if player.uid != 0:
                        notify_info(guid, player)
                    else:
                        nothing_was_found(guid)
            elif command == 'last':
                if not param:
                    player = sv_stats.get_client_stats(uid)
                    if player.uid != 0:
                        notify_last(guid, player)
                    else:
                        nothing_was_found(guid)
                else:
                    player = sv_stats.get_client_stats_by_name(param)
                    if player.uid != 0:
                        notify_last(guid, player)
                    else:
                        nothing_was_found(guid)
            elif command == 'top':
                notify_top(guid, sv_stats.get_top_stats())
    except:
        sv_custom_utils.simple_exception_info()


# Notify client to wait and retry
def notify_to_wait(guid):
    guid = int(guid)
    server.Notify(guid, '^ySpam ^yprotection. ^yWait ^ya ^ybit')


def nothing_was_found(guid):
    guid = int(guid)
    server.Notify(guid, '^yNothing ^ywas ^yfound...')


def notify_info(guid, player):
    server.Notify(guid, '^y====================================================')
    server.Notify(guid, '^y[General ^ystatistic ^yfor: ^g%s^y]' % player.last_used_name)
    server.Notify(guid, '^y[^900Accuracy^y]')
    server.Notify(guid, '^yShots: ^g%s' % player.accuracy_stats.accumulated_shots)
    server.Notify(guid, '^yHits: ^g%s' % player.accuracy_stats.accumulated_hits)
    server.Notify(guid, '^yFrags: ^g%s' % player.accuracy_stats.accumulated_frags)
    server.Notify(guid, '^yAccuracy: ^g%s' % player.accuracy_stats.accumulated_percent)
    if player.awards.has_awards():
        server.Notify(guid, '^y[^900Awards^y]')
        server.Notify(guid, '^yAimbot: ^g%s' % player.awards.mvp) if bool(player.awards.accumulated_aimbot) else None
        server.Notify(guid, '^yMvp: ^g%s' % player.awards.mvp) if bool(player.awards.accumulated_mvp) else None
        server.Notify(guid, '^ySadist: ^g%s' % player.awards.mvp) if bool(player.awards.accumulated_sadist) else None
        server.Notify(guid, '^ySurvivor: ^g%s' % player.awards.mvp) if bool(player.awards.accumulated_survivor) else None
        server.Notify(guid, '^yRipper: ^g%s' % player.awards.mvp) if bool(player.awards.accumulated_ripper) else None
        server.Notify(guid, '^yPhoe: ^g%s' % player.awards.mvp) if bool(player.awards.accumulated_phoe) else None
    server.Notify(guid, '^y====================================================')


def notify_last(guid, player):
    server.Notify(guid, '^y====================================================')
    server.Notify(guid, '^y[Latest ^ystatistic ^yfor: ^g%s^y]' % player.last_used_name)
    server.Notify(guid, '^y[^900Accuracy^y]')
    server.Notify(guid, '^yShots: ^g%s' % player.accuracy_stats.last_shots)
    server.Notify(guid, '^yHits: ^g%s' % player.accuracy_stats.last_hits)
    server.Notify(guid, '^yFrags: ^g%s' % player.accuracy_stats.last_frags)
    server.Notify(guid, '^yAccuracy: ^g%s' % player.accuracy_stats.accuracy_percent)
    server.Notify(guid, '^y====================================================')


def notify_top(guid, cache):
    server.Notify(guid, '^y====================================================')
    server.Notify(guid, '^y[Top ^ystatistics]')
    # ------------------------------------------------------------------------------------------
    aimbots = '^900AIMBOTS:'
    for idx in xrange(0, len(cache['aimbots'])):
        aimbots += ' ^y[%s. ^y%s ^y- ^y%s%%]' % (idx, cache['aimbots'][idx].last_used_name,
                                         cache['aimbots'][idx].awards.accumulated_aimbot)
        aimbots += '^y,' if idx < len(cache['aimbots']) - 1 else None
    server.Notify(guid, aimbots)
    # ------------------------------------------------------------------------------------------
    sadists = '^900SADISTS:'
    for idx in xrange(0, len(cache['sadists'])):
        sadists += ' ^y[%s. ^y%s ^y- ^y%s]' % (idx, cache['sadists'][idx].last_used_name,
                                       cache['sadists'][idx].awards.accumulated_sadist)
        sadists += '^y,' if idx < len(cache['sadists']) - 1 else None
    server.Notify(guid, sadists)
    # ------------------------------------------------------------------------------------------
    survivors = '^900SURVIVORS:'
    for idx in xrange(0, len(cache['survivors'])):
        survivors += ' ^y[%s. ^y%s ^y- ^y%s]' % (idx, cache['survivors'][idx].last_used_name,
                                         cache['survivors'][idx].awards.accumulated_survivor)
        survivors += '^y,' if idx < len(cache['survivors']) - 1 else None
    server.Notify(guid, survivors)
    # ------------------------------------------------------------------------------------------
    rippers = '^900RIPPERS:'
    for idx in xrange(0, len(cache['rippers'])):
        rippers += ' ^y[%s. ^y%s ^y- ^y%s]' % (idx, cache['rippers'][idx].last_used_name,
                                       cache['rippers'][idx].awards.accumulated_ripper)
        rippers += '^y,' if idx < len(cache['rippers']) - 1 else None
    server.Notify(guid, rippers)
    # ------------------------------------------------------------------------------------------
    phoes = '^900PHOES:'
    for idx in xrange(0, len(cache['phoes'])):
        phoes += ' ^y[%s. ^y%s ^y- ^y%s]' % (idx, cache['phoes'][idx].last_used_name,
                                     cache['phoes'][idx].awards.accumulated_phoe)
        phoes += '^y,' if idx < len(cache['phoes']) - 1 else None
    server.Notify(guid, phoes)
    # ------------------------------------------------------------------------------------------
    mvps = '^900MVPS:'
    for idx in xrange(0, len(cache['mvps'])):
        mvps += ' ^y[%s. ^y%s ^y- ^y%s]' % (idx, cache['mvps'][idx].last_used_name,
                                    cache['mvps'][idx].awards.accumulated_mvp)
        mvps += '^y,' if idx < len(cache['mvps']) - 1 else None
    server.Notify(guid, mvps)
    # ------------------------------------------------------------------------------------------
    server.Notify(guid, '^y====================================================')
