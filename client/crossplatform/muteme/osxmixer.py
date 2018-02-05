#!/usr/bin/env python3

from logging import info, error
import re
import subprocess

class OsXMixer:
    start_volume = 100
    set_volume_cmd = "osascript -e 'set volume input volume %d'"
    get_volume_cmd = "osascript -e 'input volume of (get volume settings)'"

    def __init__(self):
        try:
            self.start_volume = int(re.match("([0-9]*)", subprocess.check_output(self.get_volume_cmd,shell=True).decode()).groups()[0])
        except Exception:
            error("Unable to get initial microphone volume. Using level 100 when unmuting!", exc_info=True)
        print("Start Volume: %d" % (self.start_volume,))

    def mute(self, val=True):
        if val:
            subprocess.call(self.set_volume_cmd % (0,), shell=True)
        else:
            subprocess.call(self.set_volume_cmd % (self.start_volume,), shell=True)
