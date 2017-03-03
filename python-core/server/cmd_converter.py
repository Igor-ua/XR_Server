# -----------------------------------------------------------------------------------------------
#           Python 2.7
#           Name: cmd_converter.py
#           Description: Receives a command from the console client and executes it on the server
#                        - arg[1]   -> sends back the value of the core.CvarGetValue(arg[1])
#                        - arg[1,2] -> executes core.CvarSetValue(arg[1], int(arg[2]))
# -----------------------------------------------------------------------------------------------

# Savage API
import core
import server

# External modules
import sv_defs
import SocketServer
from multiprocessing import Process
import socket
import sv_custom_utils

HOST = "localhost"
PORT = 3322
connected_guid = 0


def init():
    core.ConsolePrint('[!]   cmd_converter is running\n')
    start_server()


class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        global connected_guid
        connected_guid += 1
        core.ConsolePrint(">   Remote client #%d connected: %s\n" % (connected_guid, self.client_address[0]))
        try:
            self.request.settimeout(3600)
            while 1:
                self.data = self.request.recv(1024)
                if not self.data:
                    break
                self.data = self.data.strip()
                params = str(self.data).split()
                # To run commands through the GameScript(guid, '!command')
                # client has to send his string in a format: 'guid?!command'
                # example: '10?!die target' -> GameScript(10, '!die target')
                if '?' in self.data:
                    exec_params = self.data.split('?')
                    if len(exec_params) > 0:
                        try:
                            guid = int(exec_params[0])
                            server.GameScript(guid, exec_params[1])
                            self.request.send("OK")
                        except:
                            core.ConsolePrint(">   Wrong params\n")
                            self.request.send("Wrong params")
                elif len(params) > 1:
                    try:
                        value = float(params[1])
                        core.ConsolePrint(">   Remote client #%d: %s\n" % (connected_guid, self.data))
                        core.CvarSetValue(params[0], value)
                        result = str("%s = %s" % (params[0], core.CvarGetValue(params[0])))
                        core.ConsolePrint(">   Result: %s\n" % result)
                        self.request.send(result)
                    except:
                        core.ConsolePrint(">   Wrong params\n")
                        self.request.send("Wrong params")
                elif len(params) == 1:
                    result = str(
                        "%s = %s | %s" % (params[0], core.CvarGetValue(params[0]), core.CvarGetString(params[0])))
                    core.ConsolePrint(">   Result: %s\n" % result)
                    self.request.send(result)
        except:
            core.ConsolePrint(">   Remote client #%d disconnected: %s\n" % (connected_guid, self.client_address[0]))


class ServerHandler:
    def __call__(self):
        core.ConsolePrint("[*]   Server is up: %s:%d\n" % (HOST, PORT))
        server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
        server.serve_forever()


def start_server():
    # server_handler = ServerHandler()
    # process = Process(target=server_handler)
    # process.start()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((HOST, PORT))
    if result != 0:
        createThread('import cmd_converter; cmd_converter.execute_thread()')


def execute_thread():
    core.ConsolePrint("[*]   Server is up: %s:%d\n" % (HOST, PORT))
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()


if __name__ == "__main__":
    init()
