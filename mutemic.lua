print(GAMEMODE_NAME)

local IP = "127.0.0.1"
local PORT = 8264

--TODO: GAMEMODE
--TODO: AddCSLuaFile for dll?
--FIXME: Beim abwesenheits specatoring wird man auch gemutet

if (SERVER) then
    util.AddNetworkString("MuteMicKilled");
    hook.Add("PlayerDeath", "MuteMicKilled", function( victim, weapon, killer )
        net.Start("MuteMicKilled");
        net.Send(victim);
    end)
    util.AddNetworkString("MuteMicSpectator");
    hook.Add("PlayerDeath", "MuteMicSpectator", function( player )
        net.Start("MuteMicSpectator");
        net.Send(player);
    end)
elseif (CLIENT) then
    local socket;
    local connected = false;
    local enabled = true;
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
        socket:Connect(IP, PORT);
    end;

    applyState = function(newState)
        if (newState ~= state and enabled) then
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
    
    /* hook.Add("PlayerDeath", "MuteMic_PlayerDeath", function (victim, inflictor, attacker)
     *     print("MuteMic: PlayerDeath");
     *     if (player == LocalPlayer()) then
     *         applyState("MUTE");
     *     end
     * end)
     *
     * hook.Add("PlayerSilentDeath", "MuteMic_PlayerSilentDeath", function (victim, inflictor, attacker)
     *     print("MuteMic: PlayerSilentDeath");
     *     if (player == LocalPlayer()) then
     *         applyState("MUTE");
     *     end
     * end)
     */

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
        applyState("SPEAK");
    end);
    
    hook.Add("PlayerSpawnAsSpectator", "MuteMic_PlayerSpawnAsSpectator", function (player)
        print("MuteMic: PlayerSpawnAsSpectator", player);
    end);

    net.Receive("MuteMicKilled", function()
        print("MuteMic: Got MuteMicKilled from server");
        if (!enabled or TTT == "PrepareRound" or TTT == "EndRound" or TTT == "unknown") then
            return;
        end
        applyState("MUTE");
    end);
    
    net.Receive("MuteMicSpectator", function()
        print("MuteMic: Got MuteMicSpectator from server");
        applyState("SPEAK");
    end);
    
    concommand.Add("mutemic",
    function (player, command, args, fullstring)
        if (args[1] == "status" or args[1] == nil) then
            print("Enabled:", enabled);
            print("Socket: ", socket);
            print("Connected: ", connected)
            print("Server:", IP .. ":" .. PORT);
            print("State: ", state);
        elseif (args[1] == "mute") then
            if !enabled then print("MuteMic is not enabled") end
            applyState("MUTE");
        elseif (args[1] == "unmute") then
            if !enabled then print("MuteMic is not enabled") end
            applyState("SPEAK");
        elseif (args[1] == "enable") then
            enabled = true;
        elseif (args[1] == "disable") then
            applyState("SPEAK");
            enabled = false;
        else
            print("Usage:");
            print("  "..command.." [status|mute|unmute|enable|disable]");
        end
    end,
    function (cmd, args)
        local tbl = {};
        table.insert(tbl, cmd.." status");
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

    pcall(init);
end
