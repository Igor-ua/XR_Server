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
import __builtin__
import sys
import time
import sv_custom_utils

this = sys.modules[__name__]

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
        return 1
    else:
        return 1


def process_private_message(sender_idx, receiver_idx, message):
    return 1


def parse_request(message, guid):
    try:
        dictionary = {"!": "", " ": ""}
        message = sv_custom_utils.replace_all(message, dictionary)
        message = message.lower()
        createThread('import sv_message_processor; sv_message_processor.process_request(%s, %s)' % (guid, message))
    except:
        sv_custom_utils.simple_exception_info()


# todo a list of clients and time control to prevent spam
#
def process_request(guid, message):
    guid = int(guid)
    try:
        current_millis = get_current_millis()
        uid = int(server.GetClientInfo(guid, INFO_UID))
        if get_client_timeout(guid) < current_millis:
            update_client_timeout(guid)
            # todo and notify client to wait and retry
        else:
            if message == this.MSG_INFO:
                player = sv_stats.get_client_stats(uid)
            elif message == this.MSG_LAST:
                player = sv_stats.get_client_stats(uid)
            elif message == this.MSG_AIM_BOTS:
                players = sv_stats.get_top_aimbots()
            elif message == this.MSG_SADISTS:
                players = sv_stats.get_top_sadists()
            elif message == this.MSG_SURVIVORS:
                players = sv_stats.get_top_survivors()
            elif message == this.MSG_MVPS:
                players = sv_stats.get_top_mvps()
            elif message == this.MSG_PHOES:
                players = sv_stats.get_top_phoes()
            elif message == this.MSG_RIPPERS:
                players = sv_stats.get_top_rippers()
    except:
        sv_custom_utils.simple_exception_info()


# CLIENT API:
#
# General info
__builtin__.MSG_INFO = "info"
# Stats from the last match
__builtin__.MSG_LAST = "last"
# Top N aimbots
__builtin__.MSG_AIM_BOTS = "aimbots"
# Top N sadists
__builtin__.MSG_SADISTS = "sadists"
# Top N mvps
__builtin__.MSG_MVPS = "mvps"
# Top N phoes
__builtin__.MSG_PHOES = "phoes"
# Top N survivors
__builtin__.MSG_SURVIVORS = "survivors"
# Top N rippers
__builtin__.MSG_RIPPERS = "rippers"
