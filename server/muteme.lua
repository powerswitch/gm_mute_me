local DEFAULT_IP = "127.0.0.1"
local DEFAULT_PORT = 8264

--TODO: Check if gamemode is terrortown (how to do that?)

if (SERVER) then
	util.AddNetworkString("MuteMeKilled");
	hook.Add("PlayerDeath", "MuteMe_PlayerDeath", function( victim, weapon, killer )
		net.Start("MuteMeKilled");
		net.Send(victim);
	end)
elseif (CLIENT) then
	local socket;
	local connected = false;
	local enabled = true;
	local spectator = false;
	local initialChatMessage = true;
	local state = "SPEAK";
	local mutedPanel;
	local TTT = "unknown";

	local init, connect, reconnect, applyState, createMutedGui, writeline, callbackConnect, callbackDisconnect, ipPortChanged;

	print("MuteMe: Initializing ...");

	init = function()
		require("bromsock");
		socket = BromSock();
		socket:SetCallbackConnect(callbackConnect);
		socket:SetCallbackDisconnect(callbackDisconnect);
		connect();
	end;

	connect = function()
		print("MuteMe: Connecting ...");
		local ip = GetConVarString("muteme_ip");
		local port = GetConVarNumber("muteme_port");
		socket:Connect(ip, port);
	end;

	reconnect = function()
		socket:Disconnect();
		connect();
	end;

	applyState = function(newState)
		if (newState ~= state) then
			state = newState;
			if (!mutedPanel) then
				createMutedGui();
			end
			if (!writeline(state) or state == "SPEAK") then
				mutedPanel:Hide()
			else
				mutedPanel:Show()
			end
		end
	end;

	createMutedGui = function()
		mutedPanel = vgui.Create("DPanel");
		mutedPanel:CenterHorizontal();
		mutedPanel:AlignBottom(130);
		mutedPanel:SetContentAlignment(5);
		mutedPanel:SetSize(110, 50);
		mutedPanel:SetBackgroundColor(Color(64, 64, 64));

		-- A red label message ( parented to background panel )
		local label = vgui.Create( "DLabel", mutedPanel );
		label:Dock( FILL )
		label:Center();
		label:SetContentAlignment(5);
		label:SetText("Muted");
		label:SetTextColor(Color(255, 0, 0));
		label:SetFont("DermaLarge");
		label:SetWrap(false);
	end;

	writeline = function(line)
		if (not connected) then
			pcall(connect);
			return false;
		end
		local packet = BromPacket();
		packet:WriteStringRaw(line .. "\n");
		socket:Send(packet, true);
		print("MuteMe wrote: " .. line);
		return true;
	end;

	callbackConnect = function(sock, ret, ip, port)
		connected = ret;
		if (not ret) then
			print("Unable to connect to MuteMe server");
			return;
		end

		print("Connected to MuteMe Server");
		writeline(state);
	end;

	callbackDisconnect = function(sock)
		print("MuteMe: server disconnected");
		connected = false;
	end;

	hook.Add("TTTPrepareRound", "MuteMe_TTTPrepareRound", function()
		TTT = "PrepareRound";
	end);

	hook.Add("TTTBeginRound", "MuteMe_TTTBeginRound", function()
		TTT = "BeginRound";

		if (! initialChatMessage) then
			return;
		end
		initialChatMessage = false;
		if connected and enabled then
			if false then RunConsoleCommand("say", "I am running MuteMe!") end;
		elseif (!enabled) then
			RunConsoleCommand("say", "My MuteMe is disabled");
		elseif socket then
			RunConsoleCommand("say", "My MuteMe Application is not running.");
		else
			RunConsoleCommand("say", "The MuteMe DLL files are not correctly installed.");
		end
	end);

	hook.Add("TTTEndRound", "MuteMe_TTTEndRound", function (result)
		print("MuteMe: TTTEndRound");
		TTT = "EndRound";
		if enabled then
			applyState("SPEAK");
		end
	end);

	net.Receive("MuteMeKilled", function()
		print("MuteMe: Got MuteMeKilled from server");
		if (!enabled or spectator or TTT == "PrepareRound" or TTT == "EndRound" or TTT == "unknown") then
			return;
		end
		applyState("MUTE");
	end);

	cvars.AddChangeCallback( "ttt_spectator_mode", function(convar_name, value_old, value_new)
		spectator = (value_new ~= "0");
		if spectator then
			print("MuteMe: Got spectator event");
			if enabled then
				applyState("SPEAK");
			end
		end
	end);

	concommand.Add("muteme",
	function (player, command, args, fullstring)
		if (args[1] == "status" or args[1] == nil) then
			print("Enabled:", enabled);
			print("Socket: ", socket);
			print("Connected: ", connected)
			print("Server:", GetConVarString("muteme_ip") .. ":" .. GetConVarNumber("muteme_port"));
			print("State: ", state);
		elseif (args[1] == "mute") then
			applyState("MUTE");
		elseif (args[1] == "unmute") then
			applyState("SPEAK");
		elseif (args[1] == "enable") then
			enabled = true;
		elseif (args[1] == "disable") then
			applyState("SPEAK");
			enabled = false;
		elseif (args[1] == "reconnect") then
			pcall(reconnect);
		elseif (args[1] == "connect") then
			connect();
		elseif (args[1] == "disconnect") then
			socket:Disconnect();
		else
			print("Usage:");
			print("  "..command.." [status|mute|unmute|enable|disable|reconnect]");
		end
	end,
	function (cmd, args)
		local tbl = {};
		table.insert(tbl, cmd.." status");
		table.insert(tbl, cmd.." reconnect");
		if state == "SPEAK" then
			table.insert(tbl, cmd.." mute");
		else
			table.insert(tbl, cmd.." unmute");
		end
		if enabled then
			table.insert(tbl, cmd.." disable");
		else
			table.insert(tbl, cmd.." enable");
		end
		return tbl;
	end, "Return muteme status or test its function. Valid arguments are: status, mute, unmute, enabled and disable") ;

	CreateClientConVar("muteme_ip", DEFAULT_IP, true, false)
	CreateClientConVar("muteme_port", DEFAULT_PORT, true, false)
	ipPortChanged = function(convar_name, value_old, value_new)
		if (value_old ~= value_new) then
			pcall(reconnect);
		end
	end;
	cvars.AddChangeCallback("muteme_ip", ipPortChanged)
	cvars.AddChangeCallback("muteme_port", ipPortChanged)

	pcall(init);
end
