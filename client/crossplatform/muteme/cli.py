#!/usr/bin/env python3

from logging import info, warning
import logging
try:
    import socketserver
except ImportError:
    import SocketServer as socketserver

from muteme.mixer import Mixer

#LISTEN = "127.0.0.1"
LISTEN = "0.0.0.0"
PORT = 8264

mixer = None

def main():
    logging.basicConfig(level=logging.DEBUG)
    setup_mixer()
    run_tcp_server()

def run_tcp_server():
    info("Serving requests on %s:%d", LISTEN, PORT)
    server = MyTCPServer((LISTEN, PORT), MyTCPHandler)
    try:
        server.serve_forever()
    except BaseException:
        server.shutdown()
    finally:
        server.server_close()
        mixer.mute(False)

def setup_mixer():
    global mixer
    mixer = Mixer()

class MyTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

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
                self.data = self.rfile.readline().strip()
            except KeyboardInterrupt:
                mixer.mute(False)
                break
            if not self.data:
                # Connection was closed
                mixer.mute(False)
                break
            if self.data == b"SPEAK":
                info("Unmuting")
                mixer.mute(False)
            elif self.data == b"MUTE":
                info("Muting")
                mixer.mute(True)
            else:
                warning("Got invalid data from %s: %s", self.client_address[0], self.data)

if __name__ == "__main__":
    import sys
    sys.exit(main())
