-- Enable or disable the mod
local mod_enabled = true


-- Message visible only to you (false) or, if host, to everyone (true)
local everyone = false


-- Name of message sender if message is for you only
local prefix = 'Bag_Counter'


-- Main message segment for non-categorized loot
local message = 'Loot Bags Secured - '


-- If set to "true," loot will be categorized by type
local categorized = false
-- Main message segment for categorized loot
local categorizedmessage = ' Bags Secured - '


-- If set to "true," instant cash loot will be counted
local littleloot = false
-- Main message segment for instant cash loot
local littlemessage = 'Instant Loot Secured - '



----------------------------------
-- Do not change anything below --
----------------------------------

-- Variable initializations for bag counting mod
if BagCounterInChat.mod_enabled == nil then
	BagCounterInChat.mod_enabled = true
else
	BagCounterInChat.mod_enabled = BagCounterInChat.mod_enabled and mod_enabled
end


BagCounterInChat = BagCounterInChat or {}


BagCounterInChat.everyone = BagCounterInChat.everyone or everyone


BagCounterInChat.prefix = BagCounterInChat.prefix or prefix


BagCounterInChat.message = BagCounterInChat.message or message


BagCounterInChat.categorized = BagCounterInChat.categorized or categorized
BagCounterInChat.categorizedmessage = BagCounterInChat.categorizedmessage or categorizedmessage


BagCounterInChat.littleloot = BagCounterInChat.littleloot or littleloot
BagCounterInChat.littlemessage = BagCounterInChat.littlemessage or littlemessage


local baglootcount = 0
local categorizedlootcount = {}
local littlelootcount = 0

-- Editted function from original Payday 2 code
function LootManager:sync_secure_loot(carry_id, multiplier_level, silent, peer_id)

	---------------------------------------------------
	-- Beginning of original function code segment 1 --
	---------------------------------------------------
	
	-- This code is from the original Payday 2 function.
	-- Changing it is not recommended
	if peer_id == 0 then
		peer_id = nil
	end

	local multiplier = tweak_data.carry.small_loot[carry_id] and managers.player:upgrade_value_by_level("player", "small_loot_multiplier", multiplier_level, 1) or 1

	table.insert(self._global.secured, {
		carry_id = carry_id,
		multiplier = multiplier,
		peer_id = peer_id
	})
	managers.hud:loot_value_updated()
	self:_check_triggers("amount")
	self:_check_triggers("total_amount")
	
	---------------------------------------------
	-- End of original function code segment 1 --
	---------------------------------------------

	-- Variable created to hold a static version of mod-information
	local BC = BagCounterInChat

	-- Checks for small loot (instant cash loot) on securing loot
	-- If loot secured is not small (i.e. a lootbag was secured)
	-- Checks appropriate mod variables, and performs appropriate message sending
	if not tweak_data.carry.small_loot[carry_id] then
		if BC.mod_enabled then
			if (not BC.categorized) then
				-- Call function for simple loot counter update
				self:provide_loot(BC)
			else
				-- Call function for categorized loot update
				self:provide_categorized_loot(BC, carry_id)
			end
		elseif baglootcount > 0 or (next(categorizedlootcount) ~= nil) then
			-- Reset variables if mod has become disabled
			-- Important for enabling/disabling the mod mid-game
			baglootcount = 0
			categorizedlootcount = {}
		end
		
		---------------------------------------------------
		-- Beginning of original function code segment 2 --
		---------------------------------------------------
		
		-- This code is from the original Payday 2 function.
		-- Changing it is not recommended
	
		self:_check_triggers("report_only")

		if not silent then
			self:_present(carry_id, multiplier)
		end
		---------------------------------------------
		-- End of original function code segment 2 --
		---------------------------------------------
		
		
	-- If collected loot is small (i.e. is an instant cash loot item)
	-- Checks mod variables and sends approrpiate message (if any)
	else
		if BC.littleloot and BC.mod_enabled then
			-- Call function for little loot message if desired
			self:provide_little_loot(BC)
		elseif littlelootcount > 0 then
			-- Reset variables if mod has become disabled
			-- Important for enabling/disabling the mod mid-game
			littlelootcount = 0
		end
	end
	
	---------------------------------------------------
	-- Beginning of original function code segment 3 --
	---------------------------------------------------
	
	-- This code is from the original Payday 2 function.
	-- Changing it is not recommended
	self:check_achievements(carry_id, multiplier)
	
	---------------------------------------------
	-- End of original function code segment 3 --
	---------------------------------------------
end


-- Function for updating simple loot count
function LootManager:provide_loot(BC)
	if managers.chat then
	
		if baglootcount == 0 then
			-- Update baglootcount by counting up the amount of non-instant cash loot
			
			-- This section is important for mid-game mod enabling/disabling OR
			-- for if someone joins a game in progress
			
			for _, data in ipairs(self._global.secured) do
				if not tweak_data.carry.small_loot[data.carry_id] and not tweak_data.carry[data.carry_id].is_vehicle then
					baglootcount = baglootcount + 1
				end
			end
		else
			-- Count the loot that was just secured
			baglootcount = baglootcount + 1
		end
		
		--Send appropriate chat message
		self:provide_count(BC, BC.message..baglootcount)
	end
	
	if next(categorizedlootcount) ~= nil then
		-- Reset categorized loot if not in use
		-- Important for mid-mission switching to categorized loot use
		categorizedlootcount = {}
	end
end

-- Function for updating categorized loot count
function LootManager:provide_categorized_loot(BC, carry_id)
	if managers.chat then
		if next(categorizedlootcount) == nil then
			-- If categorized loot has no info,
			-- Update it by counting up all loot types currently secured
			
			-- Important for mid-mission mod enabling OR
			-- for joining a mission in progress
			
			for _, data in ipairs(self._global.secured) do
				if not tweak_data.carry.small_loot[data.carry_id] and not tweak_data.carry[data.carry_id].is_vehicle then
					
					-- These two lines grab the actual in-game name of the loot
					local carry_data = tweak_data.carry[data.carry_id]
					local type_text = carry_data.name_id and managers.localization:text(carry_data.name_id)
					
					if categorizedlootcount[type_text] then
						categorizedlootcount[type_text] = categorizedlootcount[type_text] + 1
					else
						categorizedlootcount[type_text] = 1
					end
				end
			end
		
		-- Otherwise, edit appropriate loot counts
		else
			-- These two lines grab the actual in-game name of the loot
			local carry_data = tweak_data.carry[carry_id]
			local type_text = carry_data.name_id and managers.localization:text(carry_data.name_id)
			
			if categorizedlootcount[type_text] then
				categorizedlootcount[type_text] = categorizedlootcount[type_text] + 1
			else
				categorizedlootcount[type_text] = 1
			end
		end

		-- Creates the categorized loot message line-by-line
		local catmessage = '\n'
		for key, value in pairs(categorizedlootcount) do
			catmessage = catmessage..key..BC.categorizedmessage..value.."\n"
		end
		-- Function to send appropriate messages
		self:provide_count(BC, catmessage)
		
	end
	if baglootcount > 0 then
		-- Reset simple loot if not in use
		-- Important for mid-mission switching to simple loot use
		baglootcount = 0
	end
end

-- Function for updating instant cash loot count
function LootManager:provide_little_loot(BC)
	if managers.chat then
		if littlelootcount == 0 then
			-- Update littlelootcount by counting up the amount of instant cash loot
			
			-- This section is important for mid-game mod enabling/disabling OR
			-- for if someone joins a game in progress
			for _, data in ipairs(self._global.secured) do
				if tweak_data.carry.small_loot[data.carry_id] then
					littlelootcount = littlelootcount + 1
				end
			end
		else
			-- Otherwise, simple increase current count when loot is collected
			littlelootcount = littlelootcount + 1
		end
		-- Function to send appropriate messages
		self:provide_count(BC, BC.littlemessage..littlelootcount)
	end
end

-- Function for sending loot count messages
function LootManager:provide_count(BC, message)
	
	local peer = managers.network and managers.network:session() or nil
	peer = peer and peer:local_peer() or nil
	
	-- Only send to everyone if mod user is the host and
	-- wants to send to everyone
	if BC.everyone and Network:is_server() then
		managers.chat:send_message(ChatManager.GAME, peer, message)
		
	elseif peer then
		-- Otherwise, receive a personal message
		managers.chat:_receive_message(ChatManager.GAME, BC.prefix, message, Color.blue)
	end
end