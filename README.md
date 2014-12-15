MuteMe: A GarrysMod addon to mute your microphone when you die in TTT, which is useful when playing with Mumble, TeamSpeak or similar.

## Installation ##

### Server ###

Copy `server/mute_me.lua` to `<installation_directory>/garrysmod/lua/autorun/client/mute_me.lua` and `<installation_directory>/garrysmod/lua/autorun/server/mute_me.lua`

### Client ###

Install the Microsoft Visual C++ 2013 redistributable (32bit) package.

Copy `client/gmcl_bromsock_linux.dll` and `client/gmcl_bromsock_win32.dll` to `<steam_dir>/SteamApps/common/GarrysMod/garrysmod/lua/bin/` and connect to a gmod server supporting MuteMe. 

You can configure MuteMe with the `muteme` console command and the cvars `muteme_ip` and `muteme_port`.

Don't forget to run the MuteMe application while playing GarrysMod (This is currently WIP, you are on your own).
