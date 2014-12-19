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
    else:
        print("Unmuting")
    for m in mixers.items(), check_for_new_mixers():
        remove_list = []
        for dev, mixer in m:
            if mixer == None: continue
            try:
                mixer.setrec(rec)
                # If the soundcard was hotplugged while this program was running,
                # setrec fails silently. We try to reinitialize the mixer if that happens
                if (rec == 0 and sum(mixer.getrec()) != 0) or (rec != 0 and sum(mixer.getrec()) == 0):
                    remove_list.append(dev)
            except alsaaudio.ALSAAudioError as e:
                print("Warning: {} {}, removing device from list.".format(dev, e))
                remove_list.append(dev)
        for i in remove_list:
            mixers.pop(i, None)


def main():
    global mixers

    mixer_list = list_mixers()
    if mixer_list:
        print("Available muteable microphones:")
        for i in mixer_list: print("  {}".format(i))
    else:
        print("Warning: No muteable microphones found.")
        
    list(check_for_new_mixers())
    if DEVICES == "ALL":
        print("More devices will be added as they are hotplugged.")
    else:
        print("Automatically muting and unmuting the following microphones:")
        for dev in mixers.keys():
            print("  {}".format(dev))
        missing_mixers = set(DEVICES)-set(mixers.keys())
        if missing_mixers:
            print("Waiting for the following devices to be hotplugged:")
            for missing_dev in missing_mixers:
                print("  {}".format(missing_dev))
    
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
            yield (card,mixername)

def check_for_new_mixers(verbose=False):
    global mixers
    devices = set(list_mixers()) - set(mixers.keys())
    if DEVICES != "ALL":
        devices = set(DEVICES) & devices
    for device in devices:
        try:
            mixer = alsaaudio.Mixer(cardindex=device[0], control=device[1])
        except:
            continue
        try:
            mixer.getrec()
            print("Adding new device: ", device)
        except alsaaudio.ALSAAudioError as e:
            print("Warning: {} {}, ignoring.".format(device, e))
            #TODO handle that better, by:
            #mixer.setvolume(mixer_levels[0], 0, "capture")
            #mixer.setvolume(mixer_levels[0], 1, "capture")
            mixer = None
        mixers[device] = mixer
        yield device, mixer

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
