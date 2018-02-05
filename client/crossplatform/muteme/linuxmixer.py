#!/usr/bin/env python3

from logging import info, warning, error
import alsaaudio

# Mute/Unmute all microphones
DEVICES = "ALL"
# Or specify the exact names:
#DEVICES = [(0, "Capture"), (1, "Mic")]

class LinuxMixer:
    def __init__(self):
        self.mixers = {}
        mixer_list = self._list_mixers()
        if mixer_list:
            info("Available muteable microphones:")
            for i in mixer_list:
                info("  {}".format(i))
        else:
            warning("No muteable microphones found.")

        list(self._check_for_new_mixers())
        if DEVICES == "ALL":
            info("More devices will be added as they are hotplugged.")
        else:
            info("Automatically muting and unmuting the following microphones:")
            for dev in self.mixers.keys():
                info("  {}".format(dev))
            missing_mixers = set(DEVICES) - set(self.mixers.keys())
            if missing_mixers:
                warning("Waiting for the following devices to be hotplugged:")
                for missing_mixer in missing_mixers:
                    warning("  {}".format(missing_mixer))

    @staticmethod
    def _list_mixers():
        num_cards = len(alsaaudio.cards())
        for card in range(num_cards):
            for mixername in alsaaudio.mixers(card):
                mixer = alsaaudio.Mixer(control=mixername, cardindex=card)
                if "Capture Mute" not in mixer.switchcap():
                    continue
                yield (card, mixername)

    def _check_for_new_mixers(self):
        devices = set(self._list_mixers()) - set(self.mixers.keys())
        if DEVICES != "ALL":
            devices = set(DEVICES) & devices
        for device in devices:
            try:
                mixer = alsaaudio.Mixer(cardindex=device[0], control=device[1])
            except:
                continue
            try:
                mixer.getrec()
                info("Adding new device: %s", device)
            except alsaaudio.ALSAAudioError as e:
                warning("{} {}, ignoring.".format(device, e))
                #TODO handle that better, by:
                #mixer.setvolume(mixer_levels[0], 0, "capture")
                #mixer.setvolume(mixer_levels[0], 1, "capture")
                mixer = None
            self.mixers[device] = mixer
            yield device, mixer

    def mute(self, val=True):
        rec = int(not val)

        for m in self.mixers.items(), self._check_for_new_mixers():
            remove_list = []
            for dev, mixer in m:
                if mixer == None:
                    continue
                try:
                    mixer.setrec(rec)
                    # If the soundcard was hotplugged while this program was running,
                    # setrec fails silently. We try to reinitialize the mixer if that happens
                    if (rec == 0 and sum(mixer.getrec()) != 0) or (rec != 0 and sum(mixer.getrec()) == 0):
                        remove_list.append(dev)
                except alsaaudio.ALSAAudioError as e:
                    warning("{} {}, removing device from list.".format(dev, e))
                    remove_list.append(dev)
            for i in remove_list:
                self.mixers.pop(i, None)
