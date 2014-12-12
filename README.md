MuteMic: A GarrysMod addon to mute your microphone when you die in TTT, which is useful when playing with Mumble, TeamSpeak or similar.

== Installation ==

=== Server ===

Copy `server/mutemic.lua` to `<installation_directory>/garrysmod/lua/autorun/client/mutemic.lua` and `<installation_directory>/garrysmod/lua/autorun/server/mutemic.lua`

=== Client ===

Install the Microsoft Visual C++ 2013 redistributable (32bit) package.

Copy `client/gmcl_bromsock_linux.dll` and `client/gmcl_bromsock_win32.dll` to `<steam_dir>/SteamApps/common/GarrysMod/garrysmod/lua/bin/` and connect to a server supporting MuteMic. 

You can configure MuteMic with the `mutemic` console command and the cvars `mutemic_ip` and `mutemic_port`.

Don't forget to run the MuteMic application while playing GarrysMod.
