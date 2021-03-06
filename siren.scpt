(*
Campfire Siren v0.1.0
Script to wake me up in case stuff happens
****************************************************************
COPYRIGHT FETCH DEVELOPMENT, 2021
*)

tell application "Music"
	set sound volume to 80
	set volume output volume 85
	set shuffle enabled to true
	play playlist "Merciless summer"
end tell
