#!/usr/bin/python2.7

# Gets and prints the information about the current status of the server
# You can watch raw response from the linux (example):
#     echo -n -e '\x9e\x4c\x23\x00\x00\xff\xff\xce\xf2\x3b\x18\x80' | nc -u -w 1 -p 11244 94.177.253.129 11235
#
#
# Execution example: ./server_status.py
# ----------------------------------------------------------------------
# Server name:	[^yCommunity ^yServer ^c(Public)]
# Online:		[1 / 72]
# World:		[xr_greenout]
# Version:		[^900XR ^g1.3]
# ----------------------------------------------------------------------
# [^900Team 1 (human)]
# [--empty--]
# ----------------------------------------------------------------------
# [^900Team 2 (beast)]
# [--empty--]
# ----------------------------------------------------------------------
# [^900Spectators]
# [--empty--]
# ----------------------------------------------------------------------

import socket
import re

# CSP
IP = "94.177.253.129"

# Pulse:
# IP = "139.162.195.241"

# Local
# IP = "127.0.0.1"

PORT = 11235

MESSAGE = "9e4c230000ffffcef23b1880"
BINARY_MESSAGE = MESSAGE.decode('hex')

delimiter = "----------------------------------------------------------------------"


def get_server_status():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.sendto(BINARY_MESSAGE, (IP, PORT))
    data, src_address = s.recvfrom(4096)

    data = data.split("name")[1].split("\n")

    header = parse_header(data[0])
    data[0] = header['players']

    print_header(header)
    print_teams(data)
    print(delimiter)

    s.close()


def parse_header(header):
    parsed = re.split('\xfe|\xff', header)
    parsed[0] = 'name'
    result = {}
    for i in range(0, len(parsed), 2):
        result[parsed[i]] = parsed[i + 1]
    return result


def print_header(fp):
    print(delimiter)
    print("Server name:\t[%s]" % fp['name'])
    print("Online:\t\t[%s / %s]" % (fp['cnum'], fp['cmax']))
    print("World:\t\t[%s]" % fp['world'])
    print("Version:\t[%s]" % fp['ver'])


def print_teams(data):
    for i in range(0, len(data) - 1):
        if "^900Team " in data[i] or "^900Spectators" in data[i]:
            print(delimiter)
        print("[%s]" % data[i])


if __name__ == '__main__':
    get_server_status()
