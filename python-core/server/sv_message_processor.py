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
import time
import sv_custom_utils
import re
import logging
import os
from time import gmtime, strftime
import re

# Will replace all symbols from the input string that are not: '0-9A-Za-z-_() '
REGEXP_FOR_INPUT = '[^!^0-9^A-Z^a-z^\-^_^(^) ]'
# Will replace all symbols from the name that are not: '0-9A-Za-z-_() '
REGEXP_FOR_NAME = '[^0-9^A-Z^a-z^\-^_^(^) ]'

messages = {'info', 'last', 'top', 'help'}

# Generated list of GUIDs. Contains values from 0 to 128
clients_list = []

# Default timeout interval for requests (in millis)
default_timeout_interval = long(1 * 1000)


def init():
    global clients_list
    for idx in range(0, MAX_CLIENTS):
        clients_list.append([idx, long(0)])
    if not os.path.exists('python/logs'):
        os.makedirs('python/logs')


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
    try:
        # Logging a message to the file
        file_name = 'python/logs/general_chat_%s.log' % strftime("%Y-%m-%d", gmtime())
        logging.basicConfig(filename=file_name, filemode='a', level=logging.INFO)
        player_name = re.sub(REGEXP_FOR_NAME, '', server.GetClientInfo(guid, INFO_NAME))
        logging.info('[%s] %s: %s' % (message_type, player_name, re.sub(REGEXP_FOR_INPUT, '', message)))
    except:
        sv_custom_utils.simple_exception_info()
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
    try:
        # Logging a message to the file
        file_name = 'python/logs/private_chat_%s.log' % strftime("%Y-%m-%d", gmtime())
        logging.basicConfig(filename=file_name, filemode='a', level=logging.INFO)
        sender_name = re.sub(REGEXP_FOR_NAME, '', server.GetClientInfo(sender_idx, INFO_NAME))
        receiver_name = re.sub(REGEXP_FOR_NAME, '', server.GetClientInfo(receiver_idx, INFO_NAME))
        logging.info('%s -> %s: %s' % (sender_name, receiver_name, re.sub(REGEXP_FOR_INPUT, '', message)))
    except:
        sv_custom_utils.simple_exception_info()
    return 1


def parse_request(message, guid):
    try:
        # Logging a message to the file
        file_name = 'python/logs/requests_%s.log' % strftime("%Y-%m-%d", gmtime())
        logging.basicConfig(filename=file_name, filemode='a', level=logging.INFO)
        player_name = re.sub(REGEXP_FOR_NAME, '', server.GetClientInfo(guid, INFO_NAME))
        logging.info('%s: %s' % (player_name, re.sub(REGEXP_FOR_INPUT, '', message)))
    except:
        sv_custom_utils.simple_exception_info()
    try:
        replaced_message = re.sub(REGEXP_FOR_INPUT, '', message)
        msg_parts = replaced_message.split(' ')
        command = msg_parts[0].replace('!', '').lower()
        param = ''
        if len(msg_parts) > 0:
            param = msg_parts[1].lower()
        options = [int(guid), command, param]
        if command in messages:
            # process_request(guid, command, param)
            createThread('import sv_message_processor; sv_message_processor.process_request(%s)'
                         % options)
    except:
        sv_custom_utils.simple_exception_info()


def process_request(options):
    guid = options[0]
    command = options[1]
    param = options[2]
    try:
        current_millis = get_current_millis()
        uid = int(server.GetClientInfo(guid, INFO_UID))
        if get_client_timeout(guid) > current_millis:
            notify_to_wait(guid)
        else:
            core.ConsolePrint("[%s] %s: [%s]\n" % (uid, str(server.GetClientInfo(guid, INFO_NAME)), command))
            update_client_timeout(guid)
            if command == 'info':
                if not param:
                    player = sv_stats.get_client_stats(uid)
                    player.clan_tag = str(server.GetClientInfo(guid, INFO_CLANABBREV))
                    if player and player.uid != 0:
                        notify_info(guid, player)
                    else:
                        nothing_was_found(guid)
                else:
                    player = sv_stats.get_client_stats_by_name(param)
                    player.clan_tag = str(server.GetClientInfo(guid, INFO_CLANABBREV))
                    if player and player.uid != 0:
                        notify_info(guid, player)
                    else:
                        nothing_was_found(guid)
            elif command == 'last':
                if not param:
                    player = sv_stats.get_client_stats(uid)
                    player.clan_tag = str(server.GetClientInfo(guid, INFO_CLANABBREV))
                    if player and player.uid != 0:
                        notify_last(guid, player)
                    else:
                        nothing_was_found(guid)
                else:
                    player = sv_stats.get_client_stats_by_name(param)
                    player.clan_tag = str(server.GetClientInfo(guid, INFO_CLANABBREV))
                    if player and player.uid != 0:
                        notify_last(guid, player)
                    else:
                        nothing_was_found(guid)
            elif command == 'top':
                notify_top(guid, sv_stats.get_top_stats())
            elif command == 'help':
                notify_help(guid)
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
    server.Notify(guid, '')
    server.Notify(guid, '^y[General ^ystatistic ^yfor: ^w%s ^w^clan %s^ ^g%s^y]' %
                  (player.clan_tag, player.clan_id, player.last_used_name))
    server.Notify(guid, '^y[^900Accuracy^y]')
    server.Notify(guid, '^yShots: ^g%s' % player.accuracy_stats.accumulated_shots)
    server.Notify(guid, '^yHits: ^g%s' % player.accuracy_stats.accumulated_hits)
    server.Notify(guid, '^yFrags: ^g%s' % player.accuracy_stats.accumulated_frags)
    server.Notify(guid, '^yAccuracy: ^g%s%%' % player.accuracy_stats.accumulated_percent)
    if player.awards.has_awards():
        server.Notify(guid, '^y[^900Awards^y]')
        server.Notify(guid, '^yMost valuable player: ^g%s' % player.awards.accumulated_mvp)\
            if bool(player.awards.accumulated_mvp) else None
        server.Notify(guid, '^yAimbot: ^g%s' % player.awards.accumulated_aimbot)\
            if bool(player.awards.accumulated_aimbot) else None
        server.Notify(guid, '^ySadist: ^g%s' % player.awards.accumulated_sadist)\
            if bool(player.awards.accumulated_sadist) else None
        server.Notify(guid, '^ySurvivor: ^g%s' % player.awards.accumulated_survivor)\
            if bool(player.awards.accumulated_survivor) else None
        server.Notify(guid, '^yTrigardon\'s best buddy: ^g%s' % player.awards.accumulated_ripper)\
            if bool(player.awards.accumulated_ripper) else None
        server.Notify(guid, '^yPhoe: ^g%s' % player.awards.accumulated_phoe)\
            if bool(player.awards.accumulated_phoe) else None


def notify_last(guid, player):
    server.Notify(guid, '')
    server.Notify(guid, '^y[Latest ^ystatistic ^yfor: ^w%s ^w^clan %s^ ^g%s^y]' %
                  (player.clan_tag, player.clan_id, player.last_used_name))
    server.Notify(guid, '^y[^900Accuracy^y]')
    server.Notify(guid, '^yShots: ^g%s' % player.accuracy_stats.last_shots)
    server.Notify(guid, '^yHits: ^g%s' % player.accuracy_stats.last_hits)
    server.Notify(guid, '^yFrags: ^g%s' % player.accuracy_stats.last_frags)
    server.Notify(guid, '^yAccuracy: ^g%s%%' % player.accuracy_stats.accuracy_percent)


def notify_top(guid, cache):
    server.Notify(guid, '')
    server.Notify(guid, '^y[Top ^ystatistics]')
    # ------------------------------------------------------------------------------------------
    # cache structure: cache = {'aimbots', 'sadists', 'survivors', 'rippers', 'phoes', 'mvps'}
    # ------------------------------------------------------------------------------------------
    template = ' ^w[ ^900%s ^w]  ^w^clan %s^  ^g%s^y\n'
    aimbots = '^cAimbots:\n'
    for idx in xrange(0, len(cache['aimbots'])):
        aimbots += template % (cache['aimbots'][idx].awards.accumulated_aimbot,
                               cache['aimbots'][idx].clan_id, cache['aimbots'][idx].last_used_name)
    server.Notify(guid, aimbots)
    # ------------------------------------------------------------------------------------------
    sadists = '^cSadists:\n'
    for idx in xrange(0, len(cache['sadists'])):
        sadists += template % (cache['sadists'][idx].awards.accumulated_sadist,
                               cache['sadists'][idx].clan_id, cache['sadists'][idx].last_used_name)
    server.Notify(guid, sadists)
    # ------------------------------------------------------------------------------------------
    survivors = '^cSurvivors:\n'
    for idx in xrange(0, len(cache['survivors'])):
        survivors += template % (cache['survivors'][idx].awards.accumulated_survivor,
                               cache['survivors'][idx].clan_id, cache['survivors'][idx].last_used_name)
    server.Notify(guid, survivors)
    # ------------------------------------------------------------------------------------------
    rippers = '^cTrigardon\'s ^cbest ^cbuddy:\n'
    for idx in xrange(0, len(cache['rippers'])):
        rippers += template % (cache['rippers'][idx].awards.accumulated_ripper,
                               cache['rippers'][idx].clan_id, cache['rippers'][idx].last_used_name)
    server.Notify(guid, rippers)
    # ------------------------------------------------------------------------------------------
    phoes = '^cPhoes:\n'
    for idx in xrange(0, len(cache['phoes'])):
        phoes += template % (cache['phoes'][idx].awards.accumulated_phoe,
                               cache['phoes'][idx].clan_id, cache['phoes'][idx].last_used_name)
    server.Notify(guid, phoes)
    # ------------------------------------------------------------------------------------------
    mvps = '^cMVPs:\n'
    for idx in xrange(0, len(cache['mvps'])):
        mvps += template % (cache['mvps'][idx].awards.accumulated_mvp,
                             cache['mvps'][idx].clan_id, cache['mvps'][idx].last_used_name)
    server.Notify(guid, mvps)
    # ------------------------------------------------------------------------------------------


def notify_help(guid):
    server.Notify(guid, '')
    server.Notify(guid, '^900|   ^900Instagib ^900Mode ^900Information:')
    server.Notify(guid, '^900|   ^900General:')
    server.Notify(guid, '^900| ^yGame ^ystarts ^ywhen ^y70% ^yare ^yready ^y(press ^yF3)')
    server.Notify(guid, '^900| ^yWinner: ^yteam ^ythat ^yfirst ^ygets ^ya ^yfrag ^ylimit.')
    server.Notify(guid, '^900| ^yWinner: ^yteam ^ythat ^yhas ^ymore ^yfrags ^yby ^ythe ^yend.')
    server.Notify(guid, '^900|   ^900Physics:')
    server.Notify(guid, '^900| ^yIncreased ^yplayer ^yspeed')
    server.Notify(guid, '^900| ^ySprint ^yspeed ^yis ^yoff. ^ySpeed ^yis ^yconstant')
    server.Notify(guid, '^900| ^yStamina ^yis ^yoff')
    server.Notify(guid, '^900| ^yIncreased ^ycoil ^ydmg ^y(500)')
    server.Notify(guid, '^900| ^yReviving ^yand ^yteleporting ^yin ^y1 ^ysecond ^yafter ^ythe ^ydeath')
    server.Notify(guid, '^900|   ^900Statistics:')
    server.Notify(guid, '^900| ^yStats ^yare ^ybeing ^yupdated ^yevery ^yround')
    server.Notify(guid, '^900| ^yStats ^yare ^ybound ^yto ^yyour ^yUIDs')
    server.Notify(guid, '^900|   ^900Items:')
    server.Notify(guid, '^900| ^yEvery ^y5, ^y7, ^y10 ^yfrags ^ygive ^yyou ^ymist, ^ysensor, ^yreloc.')
    server.Notify(guid, '^900|   ^900Available stats commands:')
    server.Notify(guid, '^900| ^y!info ^y- ^ygeneral ^yinfo ^yabout ^yyour ^ycurrent ^yUID')
    server.Notify(guid, '^900| ^y!info ^y<part ^yof ^ythe ^ynick> - ^y(ex: ^y!info ^yxr_pla)')
    server.Notify(guid, '^900| ^y!last ^yyour ^ystats ^yfrom ^ythe ^ylast ^yround')
    server.Notify(guid, '^900| ^y!last ^y<part ^yof ^ythe ^ynick> - ^y(ex: ^y!last ^yxr_pla)')
    server.Notify(guid, '^900| ^y!top ^y- ^yTop5 players for every stat.')
    server.Notify(guid, '')
