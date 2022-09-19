if not MenuHelperHelper then return end

BagCounterInChat = {
	mod_enabled = true,
	div1 = '_ 20',
	everyone = false,
	div2 = '_ 20',
	prefix = 'Bag_Counter',
	div3 = '_ 20',
	message = 'Loot Bags Secured - ',
	div4 = '_ 20',
	categorized = false,
	categorizedmessage = ' Bags Secured - ',
	div5 = '_ 20',
	littleloot = false,
	littlemessage = 'Instant Loot Secured - '
}

MenuHelperHelper._tweaks = {
	mod_enabled = { priority = 13 },
	div1 = { priority = 12 },
	everyone = { priority = 11 },
	div2 = { priority = 10 },
	prefix = { priority = 9 },
	div3 = { priority = 8 },
	message = { priority = 7 },
	div4 = { priority = 6 },
	categorized = { priority = 5 },
	categorizedmessage = { priority = 4 },
	div5 = { priority = 3 },
	littleloot = { priority = 2 },
	littlemessage = { priority = 1 },
	default = { 
		save_only_changed = true
	}
}

MenuHelperHelper:CreateMenu(BagCounterInChat, 'bc_chat', 'Bag_Counter_In_Chat.txt', function(settings)
	BagCounterInChat = settings
end)

local thisPath
local thisDir
local function Dirs()
	thisPath = debug.getinfo(2, "S").source:sub(2)
	thisDir = string.match(thisPath, '.*/')
end
Dirs()
Dirs = nil

Hooks:Add("LocalizationManagerPostInit", "BagCounterInChat", function(loc)
	LocalizationManager:load_localization_file(thisDir..'Bag_loc.json')
end)