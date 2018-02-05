#!/usr/bin/env python3

from ctypes import cast, POINTER
import comtypes
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, CLSID_MMDeviceEnumerator, IMMDeviceEnumerator, EDataFlow, ERole

class WindowsMixer:
    @staticmethod
    def _get_microphones():
        deviceEnumerator = comtypes.CoCreateInstance(
            CLSID_MMDeviceEnumerator,
            IMMDeviceEnumerator,
            comtypes.CLSCTX_INPROC_SERVER)
        microphones = deviceEnumerator.GetDefaultAudioEndpoint(
            EDataFlow.eCapture.value, ERole.eConsole.value)
        return microphones

    def __init__(self):
        devices = self._get_microphones()

        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

        self.microphone_volume = cast(interface, POINTER(IAudioEndpointVolume))

    def mute(self, val=True):
        return self.microphone_volume.SetMute(val, None)

    def get_mute(self):
        return self.microphone_volume.GetMute()
