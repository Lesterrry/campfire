(*
Campfire Zipline v0.1.0
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
		delay 3
		-- Reference current page
		set myDoc to document of front window
		-- Get the source of the page
		set mySrc to source of myDoc
		close document of front window
		-- Look for seed inside the source
		mySrc contains seed
	end tell
end run
