#!/usr/bin/env python3

from logging import warning
from platform import system

platform = system()

if platform == "Linux":
    from muteme.linuxmixer import LinuxMixer as Mixer
elif platform == "Windows":
    from muteme.windowsmixer import WindowsMixer as Mixer
elif platform == "Darwin":
    from muteme.osxmixer import OsXMixer as Mixer
else:
    warning("Your platform (%s) is not known to us. Trying to load a mixer anyway." % (platform,))
    for _ in (0,):
        try:
            from muteme.windowsmixer import WindowsMixer as Mixer
        except ImportError:
            pass
        else:
            warning("Using Windows mixer.")
            break
        try:
            from muteme.linuxmixer import LinuxMixer as Mixer
        except ImportError:
            raise
        else:
            warning("Using Linux mixer.")
            break
        try:
            from muteme.osxmixer import OsXMixer as Mixer
        except ImportError:
            pass
        else:
            warning("Using Mac OS X mixer.")
            break
        raise Exception("No mixer for your platform (%s) found." % (platform,))

def main():
    from humanfriendly import coerce_boolean

    user_input = coerce_boolean(sys.argv[1]) if len(sys.argv) > 1 else True

    if user_input:
        print("Muting.")
    else:
        print("Unmuting.")

    mixer = Mixer()
    return mixer.mute(user_input)


if __name__ == "__main__":
    import sys
    sys.exit(main())
    del sys

del main
del platform
del system
del warning
