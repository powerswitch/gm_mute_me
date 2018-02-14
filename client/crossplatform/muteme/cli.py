#!/usr/bin/env python3

import logging

from muteme.mixer import Mixer
from muteme.network import AsyncTcpServer

mixer = None

def main():
    logging.basicConfig(level=logging.DEBUG)
    setup_mixer()

    tcp_server = AsyncTcpServer(mute_callback)
    tcp_server.run_standalone()
    mixer.mute(False)

def setup_mixer():
    global mixer
    mixer = Mixer()

def mute_callback(mute):
    mixer.mute(mute)


if __name__ == "__main__":
    import sys
    sys.exit(main())
