#!/usr/bin/env python3

import sys, os, re
import subprocess
try:
    import socketserver
except:
    import SocketServer as socketserver

# Mute/Unmute all microphones
DEVICES = "ALL"
# Or specify the exact names:
#DEVICES = [(0, "Capture"), (1, "Mic")]

LISTEN = "127.0.0.1"
#LISTEN = "0.0.0.0"
PORT = 8261

mixers = {}
startVolume = 100

class MyTCPHandler(socketserver.StreamRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def handle(self):
        # self.request is the TCP socket connected to the client
        while True:
            try:
                self.data = self.rfile.readline().strip().decode("utf-8")
            except: # KeyboardInterrupt and others
                break
            if not self.data:
                # Connection was closed
                set_mute(False)
                break
            if self.data == "SPEAK":
                set_mute(False)
            elif self.data == "MUTE":
                set_mute(True)
            else:
                print("Got invalid data from {}:{}".format(self.client_address[0], self.data))

def set_mute(mute):
    rec = int(mute == False)
    if mute:
        print("Muting")
        subprocess.call("osascript -e 'set volume input volume 0'",shell=True)
    else:
        print("Unmuting")
        subprocess.call("osascript -e 'set volume input volume {}'".format(startVolume),shell=True)



def main():
    global mixers
    global startVolume
    startVolume = re.match("([0-9]*)",subprocess.check_output("osascript -e 'input volume of (get volume settings)'",shell=True).decode()).groups()[0]
    print("Start Volume: {}".format(startVolume))
    print("Serving requests on {}:{}".format(LISTEN, PORT))
    server = socketserver.TCPServer((LISTEN, PORT), MyTCPHandler)
    try:
        server.serve_forever()
    except:
        server.shutdown()
        set_mute(False)

if __name__ == "__main__":
    sys.exit(main())
