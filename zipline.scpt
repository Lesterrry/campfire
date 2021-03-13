(*
Campfire Zipline v0.2.0
Website data parser to link with Campfire
****************************************************************
COPYRIGHT FETCH DEVELOPMENT, 2021
*)

on run argv
	tell application "Safari"
		-- Get parameters from argv 
		set loc to item 1 of argv
		set soldout_key to item 2 of argv
		set in_stock_key to item 3 of argv
		-- Open website in Safari
		open location loc
		set i to 0
		set res to "none"
		repeat while true
			set i to i + 1
			-- Get the source of the page
			set mySrc to source of current tab of window 1
			--Check until the page is loaded or timeout
			if mySrc contains in_stock_key then
				set res to "in_stock"
				exit repeat
			else if mySrc contains soldout_key then
				set res to "sold_out"
				exit repeat
			else if i is equal to 20 then
				set res to "time_out"
				exit repeat
			end if
			delay 0.5
		end repeat
		close document of front window
		res
	end tell
end run
