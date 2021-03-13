(*
Campfire Zipline v0.1.1
Website data parser to link with Campfire
****************************************************************
COPYRIGHT FETCH DEVELOPMENT, 2021
*)

on run argv
	tell application "Safari"
		-- Get parameters from argv 
		set loc to item 1 of argv
		set seed to item 2 of argv
		-- Open website in Safari
		open location loc
		set i to 0
		repeat while true
			set i to i + 1
			-- Get the source of the page
			set mySrc to source of current tab of window 1
			--Check until the page is loaded or timeout
			if (mySrc is not equal to "") or (i is equal to 20) then
				delay 1
				exit repeat
			end if
			delay 0.5
		end repeat
		close document of front window
		-- Look for seed inside the source
		mySrc contains seed
	end tell
end run
