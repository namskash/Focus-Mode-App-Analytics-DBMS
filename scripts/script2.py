import mysql.connector
from datetime import date, timedelta
from random import randint,choices,choice,sample

def getTime(time):			# converts
	#time = time / 60
	hours = int(time / 60)
	minutes = int(time % 60)
	seconds = int((time / 60) % 60)

	return str(hours) + ":" + str(minutes) + ":" + str(seconds)


mydb = mysql.connector.connect(
	host="localhost",
	user="namskash",
	password="abcd",
	database="focusModeDBMS"
)

mycursor = mydb.cursor(buffered=True)

#"""
# SESSIONS + BREAKS
date1, date2 = date(2021,11,4), date.today()
dates = [date1]
while(date1 <= date2):
	date1 += timedelta(days = randint(0,4))
	dates.append(date1)

dates = list(choices(dates,k=100))	# k=number of dates needed
#print(len(dates))

sessions = 1
breaks = 1

for i in range(100):	# entry into 
	sessionID = "SES" + "0" * (3 - len(str(sessions))) + str(sessions)
	sessions += 1
	
	sessionDate = dates[i]
	sessionStartTime = randint(30,1410)	# 1440 is midnight in minutes
	sessionEndTime = randint(sessionStartTime + 30,sessionStartTime + 180)	# half hour to 3 hours
	sessionDuration = sessionEndTime - sessionStartTime
	mycursor.execute("insert into SESSIONS values (%s,%s,%s,%s,%s)",(sessionID,sessionDate,getTime(sessionStartTime),getTime(sessionEndTime),sessionDuration))
	
	breakID = "BRK" + "0" * (3 - len(str(breaks))) + str(breaks)
	breaks += 1

	breakDate = dates[i]	# same as session
	breakStartTime = randint(sessionStartTime + 20,sessionEndTime - 10)
	breakEndTime = randint(breakStartTime + 5,sessionEndTime)
	breakDuration = breakEndTime - breakStartTime
	mycursor.execute("insert into BREAKS values (%s,%s,%s,%s,%s,%s)",(breakID,breakDate,getTime(breakStartTime),getTime(breakEndTime),breakDuration,sessionID))

	for j in range(randint(1,5)):
		try:
			breakID = "BRK" + "0" * (3 - len(str(breaks))) + str(breaks)
			breaks += 1
			breakStartTime = randint(breakEndTime + 5,sessionEndTime - 30)
			breakEndTime = randint(breakStartTime + 5,sessionEndTime)
			breakDuration = breakEndTime - breakStartTime
			mycursor.execute("insert into BREAKS values (%s,%s,%s,%s,%s,%s)",(breakID,breakDate,getTime(breakStartTime),getTime(breakEndTime),breakDuration,sessionID))
		except:
			pass
	
mydb.commit()

# APPS
sessionAppList = ['MS Word','MS PowerPoint','MS Excel','VS Code','Eclipse','Oracle VirtualBox','Ubuntu 22.04 VM']
breakAppList = ['Google Chrome','YouTube','Prime Video','Netflix','Solitaire','Hangman']
timers = ["30","45"]
timersMAX = ["45","60"]

for i in range(len(sessionAppList)):
	appID = "APP" + "0" * (3 - len(str(i+1))) + str(i+1)
	mycursor.execute("insert into APPS values (%s,%s,%s,%s,%s)",(appID,sessionAppList[i],1,None,None))

id = len(sessionAppList) + 1
for i in range(len(breakAppList)):
	appID = "APP" + "0" * (3 - len(str(i+id))) + str(i+id)
	mycursor.execute("insert into APPS values (%s,%s,%s,%s,%s)",(appID,breakAppList[i],0,choice(timers) + " mins",choice(timersMAX) + " mins"))

mydb.commit()

mycursor.execute("select * from APPS")
res = mycursor.fetchall()

# WARNINGS
warnings = 0
mycursor.execute("select count(breakID) from BREAKS")
breaksSQL = mycursor.fetchall()

# SESSION_APPS
mycursor.execute("select sessionID from SESSIONS")
temp = mycursor.fetchall()
sessionIDs = []
for i in temp:
	sessionIDs.append(i[0])	#// to convert from tuple(tuple()) to a normal list

mycursor.execute("select appID from APPS where privileged = 0x01")
temp = mycursor.fetchall()
sessionAppIDs = []
for i in temp:
	sessionAppIDs.append(i[0])	#// to convert from tuple(tuple()) to a normal list

for i in range(len(sessionIDs)):
	apps_per_session = randint(1,4)
	temp = set(sample(sessionAppIDs,apps_per_session))	# n random apps, unique

	for j in temp:
		mycursor.execute("insert into SESSION_APPS values (%s,%s)",(sessionIDs[i],j))
#"""

# BREAK_APPS
mycursor.execute("select breakID from BREAKS")
temp = mycursor.fetchall()
breakIDs = []
for i in temp:
	breakIDs.append(i[0])	#// to convert from tuple(tuple()) to a normal list

mycursor.execute("select appID from APPS where privileged = 0x00")
temp = mycursor.fetchall()
breakAppIDs = []
for i in temp:
	breakAppIDs.append(i[0])	#// to convert from tuple(tuple()) to a normal list

for i in range(len(breakIDs)):
	apps_per_break = randint(1,4)
	temp = set(sample(breakAppIDs,apps_per_break))	# n random apps, unique

	for j in temp:
		mycursor.execute("insert into BREAK_APPS values (%s,%s)",(breakIDs[i],j))

mydb.commit()
