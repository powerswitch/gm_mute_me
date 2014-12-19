#!/usr/bin/env python3

import sys, os
import alsaaudio
import socketserver

# Mute/Unmute all microphones
DEVICES = "ALL"
# Or specify the exact names:
#DEVICES = [(0, "Capture"), (1, "Mic")]

LISTEN = "127.0.0.1"
#LISTEN = "0.0.0.0"
PORT = 8264

mixers = {}

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
            self.data = self.rfile.readline().strip().decode("utf-8")
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
    if mute:
        print("Muting")
    else:
        print("Unmuting")
    remove_list = []
    for dev, mixer in mixers.items():
        try:
            mixer.setrec(int(mute == False))
        except alsaaudio.ALSAAudioError as e:
            print("Error: {} {}, ignoring.".format(dev, e))
            #TODO handle that better, by:
            #mixer.setvolume(mixer_levels[0], 0, "capture")
            #mixer.setvolume(mixer_levels[0], 1, "capture")
            remove_list.append(dev)
    for i in remove_list:
        mixers.pop(i)

def main():
    global DEVICES, mixers
    mixer_list = list_mixers()
    if mixer_list:
        print("Available mutable microphones:")
        for i in mixer_list: print("  {}".format(i))
    else:
        print("No mutable microphones found, sorry.")
    if DEVICES == "ALL":
        DEVICES = mixer_list
    for card, mixer in set(DEVICES) & set(mixer_list):
        mixers[(card,mixer)] = alsaaudio.Mixer(cardindex=card, control=mixer)
    if not mixers:
        print("No microphones to mute. Please adjust the DEVICES variable.")
        return False
    print("Automatically muting and unmuting the following microphones:")
    for dev in mixers.keys(): print("  {}".format(dev))
        
    
    print("Serving requests on {}:{}".format(LISTEN, PORT))
    server = socketserver.TCPServer((LISTEN, PORT), MyTCPHandler)
    try:
        server.serve_forever()
    except:
        server.shutdown()
        set_mute(False)
    
def list_mixers():
    ret = []
    num_cards = len(alsaaudio.cards())
    for card in range(num_cards):
        for mixername in alsaaudio.mixers(card):
            mixer = alsaaudio.Mixer(control=mixername, cardindex=card)
            if "Capture Mute" not in mixer.switchcap():
                continue
            ret.append((card,mixername))
    return ret
        

def pulseaudio_does_not_work():
    import dbus
    import logging as log
    def get_bus(srv_addr=None, dont_start=False):
        srv_addr = get_bus_address()
        log.debug('Got pa-server bus from dbus: %s', srv_addr)
        # print(dbus.connection.Connection(srv_addr)\
        #   .get_object(object_path='/org/pulseaudio/core1')\
        #   .Introspect(dbus_interface='org.freedesktop.DBus.Introspectable'))
        return dbus.connection.Connection(srv_addr)

    def get_bus_address():
        srv_addr = os.environ.get('PULSE_DBUS_SERVER')
        if not srv_addr and os.access('/run/pulse/dbus-socket', os.R_OK | os.W_OK):
            # Well-known system-wide daemon socket
            srv_addr = 'unix:path=/run/pulse/dbus-socket'
        if not srv_addr:
            srv_addr = dbus.SessionBus().get_object(
                'org.PulseAudio1', '/org/pulseaudio/server_lookup1')\
                .Get('org.PulseAudio.ServerLookup1',
                'Address', dbus_interface='org.freedesktop.DBus.Properties')
        return srv_addr
    bus = get_bus()
    
    recordStreams = dbus.Interface(bus.get_object(bus_name="org.PulseAudio.Core1", object_path="/org/pulseaudio/core1", introspect=True), 'org.freedesktop.DBus.Properties').GetAll("org.PulseAudio.Core1")['RecordStreams']
    
    for stream in recordStreams:
        client = dbus.Interface(bus.get_object(bus_name="org.PulseAudio.Core1", object_path=stream, introspect=True), 'org.freedesktop.DBus.Properties').GetAll("org.PulseAudio.Core1.Stream")["Client"]
        application_name_dbus = dbus.Interface(bus.get_object(bus_name="org.PulseAudio.Core1", object_path=client, introspect=True), 'org.freedesktop.DBus.Properties').GetAll("org.PulseAudio.Core1.Client")["PropertyList"]["application.name"]
        
        application_name = "".join(chr(b) for b in application_name_dbus if b != 0)
        
        if application_name == "Mumble":
            print(dbus.Interface(bus.get_object(bus_name="org.PulseAudio.Core1.Stream", object_path=stream, introspect=True), 'org.freedesktop.DBus.Properties').Get("org.PulseAudio.Core1.Stream", "Mute"))

if __name__ == "__main__":
    sys.exit(main())
