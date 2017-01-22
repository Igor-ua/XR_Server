# ----------------------------------------------------
#           Python 2.7
#           Name: console_client.py
# ----------------------------------------------------

# External modules
import socket
import sys

HOST, PORT = "localhost", 3322
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((HOST, PORT))
    while 1:
        try:
            print("command ->")
            line = sys.stdin.readline()
        except KeyboardInterrupt:
            break

        if not line:
            break

        sock.send(line)
        received = sock.recv(1024)
        print("Response: %s" % received)
finally:
    print("Client is closing connection")
    sock.close()
