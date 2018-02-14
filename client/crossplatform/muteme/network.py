#!/usr/bin/env python3

from logging import info, warning
import asyncio

#LISTEN = "127.0.0.1"
LISTEN = "0.0.0.0"
PORT = 8264

class AsyncTcpServer:
    def __init__(self, mute_callback, event_loop=None):
        self.mute_callback = mute_callback
        self.event_loop = event_loop

        if self.event_loop is None:
            try:
                self.event_loop = asyncio.get_event_loop()
            except RuntimeError:
                self.event_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.event_loop)

    def run_standalone(self):
        tcp_server = self.run()

        # Serve requests until Ctrl+C is pressed
        try:
            self.event_loop.run_forever()
        except KeyboardInterrupt:
            pass

        # Close the server
        tcp_server.close()
        self.event_loop.run_until_complete(tcp_server.wait_closed())

        # Stop running tasks (i.e. open connections)
        for t in asyncio.Task.all_tasks(self.event_loop):
            t.cancel()

        # Shut down event loop
        self.event_loop.run_until_complete(self.event_loop.shutdown_asyncgens())
        self.event_loop.close()

    def run(self):
        server_coroutine = asyncio.start_server(self.handle_client_connection, LISTEN, PORT, loop=self.event_loop)
        tcp_server = self.event_loop.run_until_complete(server_coroutine)

        print('Serving on {}'.format(tcp_server.sockets[0].getsockname()))

        return tcp_server

    async def handle_client_connection(self, reader, writer):
        while True:
            data = await reader.readline()

            if not data:
                info("Client connection was closed")
                writer.close()
                self.mute_callback(False)
                break

            if data == b"SPEAK\n":
                info("Unmuting")
                self.mute_callback(False)
            elif data == b"MUTE\n":
                info("Muting")
                self.mute_callback(True)
            else:
                warning("Got invalid data from %s: %s", writer.get_extra_info("peername"), data)


def _main():
    tcp_server = AsyncTcpServer(_mute_cb)
    tcp_server.run_standalone()

def _mute_cb(mute):
    if mute:
        print("Muting")
    else:
        print("Unmuting")

if __name__ == "__main__":
    import sys
    sys.exit(_main())
