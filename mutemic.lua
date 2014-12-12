print(GAMEMODE_NAME)

local DEFAULT_IP = "127.0.0.1"
local DEFAULT_PORT = 8264

--TODO: GAMEMODE
--TODO: AddCSLuaFile for dll?

if (SERVER) then
    util.AddNetworkString("MuteMicKilled");
    hook.Add("PlayerDeath", "MuteMic_PlayerDeath", function( victim, weapon, killer )
        net.Start("MuteMicKilled");
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
    
    local init, connect, applyState, createMutedGui, writeline, callbackConnect, callbackDisconnect;
    
    print("MuteMic: Initializing ...");

    init = function()
        require("bromsock");
        socket = BromSock();
        socket:SetCallbackConnect(callbackConnect);
        socket:SetCallbackDisconnect(callbackDisconnect);
        connect();
    end;
    
    connect = function()
        print("MuteMic: Connecting ...");
        local ip = GetConVarString("mutemic_ip");
        local port = GetConVarNumber("mutemic_port");
        socket:Connect(ip, port);
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
        print("MuteMic wrote: " .. line);
        return true;
    end;

    callbackConnect = function(sock, ret, ip, port)
        connected = ret;
        if (not ret) then
            print("Unable to connect to MuteMic server");
            return;
        end
        
        print("Connected to MuteMic Server");
        writeline(state);
    end;

    callbackDisconnect = function(sock)
        print("MuteMic: server disconnected");
        connected = false;
    end;
    
    hook.Add("TTTPrepareRound", "MuteMic_TTTPrepareRound", function()
        TTT = "PrepareRound";
    end);
    
    hook.Add("TTTBeginRound", "MuteMic_TTTBeginRound", function()
        TTT = "BeginRound";
        
        if (! initialChatMessage) then
            return;
        end
        initialChatMessage = false;
        if connected and enabled then
            if false then RunConsoleCommand("say", "I am running MuteMic!") end;
        elseif (!enabled) then
            RunConsoleCommand("say", "My MuteMic is disabled");
        elseif socket then
            RunConsoleCommand("say", "My MuteMic is not connected.");
        else
            RunConsoleCommand("say", "MuteMic is not installed on my system");
        end
    end);
    
    hook.Add("TTTEndRound", "MuteMic_TTTEndRound", function (result)
        print("MuteMic: TTTEndRound");
        TTT = "EndRound";
        if enabled then
            applyState("SPEAK");
        end
    end);
    
    net.Receive("MuteMicKilled", function()
        print("MuteMic: Got MuteMicKilled from server");
        if (!enabled or spectator or TTT == "PrepareRound" or TTT == "EndRound" or TTT == "unknown") then
            return;
        end
        applyState("MUTE");
    end);
    
    cvars.AddChangeCallback( "ttt_spectator_mode", function(convar_name, value_old, value_new)
        spectator = (value_new ~= "0");
        if spectator then
            print("MuteMic: Got spectator event");
            if enabled then
                applyState("SPEAK");
            end
        end
    end);
    
    concommand.Add("mutemic",
    function (player, command, args, fullstring)
        if (args[1] == "status" or args[1] == nil) then
            print("Enabled:", enabled);
            print("Socket: ", socket);
            print("Connected: ", connected)
            print("Server:", GetConVarString("mutemic_ip") .. ":" .. GetConVarNumber("mutemic_port"));
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
            pcall(function()
                socket:Disconnect();
                connect();
            end);
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
    end, "Return mutemic status or test its function. Valid arguments are: status, mute, unmute, enabled and disable") ;

    CreateClientConVar("mutemic_ip", DEFAULT_IP, true, false)
    CreateClientConVar("mutemic_port", DEFAULT_PORT, true, false)
    pcall(init);
end
