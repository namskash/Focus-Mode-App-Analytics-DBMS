Focus mode DBMS

Tables:
	* Sessions
	* Breaks
	* Apps
	* Warnings

Relations:
	* Session_breaks
	* Session_apps
	* Break_apps

Descriptions:
	#1 Sessions: 
	// A history of all sessions
		* sessionID (pk)
		* date
		* startTime
		* endTime
		* duration (automatic set?)
	
	#2 Breaks:
	// A history of all breaks
		* breakID
		* date
		* startTime
		* endTime
		* allowedDuration
		* actualDuration (automatic set?)
	
	#3 Apps:
	// A list of all apps on device
		* appID
		* privileged (yes/no)
		* timers (if not privileged)
		* timerMAX

	#4 Warnings:
	// Timer limit reached
		* appID
		* date
		* snooze (amount of time)

	# Session_breaks:
	// Relationship between sessions and breaks. 1:N relatiosnship
		* sessionID
		* breakID

	# Session_apps:
	// Apps allowed during focus mode session. i.e the app(s) you had to focus on
		* sessionID
		* appID
	
	# Break_apps:
	// Apps used during breaks
		* breakID
		* appID
