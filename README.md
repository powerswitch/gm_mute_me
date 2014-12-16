MuteMe: A GarrysMod addon to mute your microphone when you die in TTT, which
is useful when playing with Mumble, TeamSpeak or similar.

## Installation ##

### Server ###

Copy `server/mute_me.lua` to `<installation_directory>/garrysmod/lua/autorun/mute_me.lua`
and restart the server.

### Client ###

#### Windows ####

Install the Microsoft Visual C++ 2013 redistributable (32bit) package.
Then copy `client/gmcl_bromsock_win32.dll` to
`<steam_dir>/SteamApps/common/GarrysMod/garrysmod/lua/bin/` (you may need to
create that directory). Next, run the MuteMe desktop application before
starting GarrysMod.

#### Linux ####

Copy `client/gmcl_bromsock_linux.dll` to
`<steam_dir>/SteamApps/common/GarrysMod/garrysmod/lua/bin/` (you may need to
create that directory). Next, run the MuteMe desktop application from
`clients/linux` in this repository, before starting GarrysMod. You may need to
adapt it to your system if you have a more complicated sound card setup.


#### Mac OS X ####

No work done here, sorry. You can try to compile the gm_bromsock library on
your own and see if it works. Feel free to send a pull request if you do.


## Configuration ##

You can configure MuteMe with the `muteme` console command and the cvars
`muteme_ip` and `muteme_port`. Also, don't forget to run the MuteMe
application while playing GarrysMod.


## Troubleshooting ##

TODO
