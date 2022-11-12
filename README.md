# Focus mode DBMS
A focus mode database, that keeps track of focus sessions, apps used, breaks taken, and app timers.
This project uses MySQL and Python to simulate the features and functionalities of a focus mode assist app.
The aim of this project is to enhance our understanding of MySQL and to create a minimalistic UI for the app using tkinter in Python.

## Tables:
+ Sessions
+ Breaks
+ Apps

## Relations:
+ Session_breaks
+ Session_apps
+ Break_apps

## ***Table Descriptions:***
### 1. Sessions: 
*A history of all sessions*
+ sessionID (pk)
+ date
+ startTime
+ endTime
+ duration

### 2. Breaks:
*A history of all breaks*
+ breakID (pk)
+ date
+ startTime
+ endTime
+ breakDuration
+ sessionID (fk)

### 3. Apps:
*A list of all apps on device*
+ appID
+ appName
+ privileged (yes/no)
+ timer (if not privileged)
+ timerMAX

## ***Relationship Descriptions:***
### 4. Session_apps:
*Apps allowed during focus mode session. i.e the app(s) you had to focus on*
+ sessionID
+ appID

### 5. Break_apps:
*Apps used during breaks*
+ breakID
+ appID
