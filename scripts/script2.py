import mysql.connector
from datetime import date, timedelta
from random import randint,choices,choice

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
	#print(date1)

dates = list(choices(dates,k=100))	# k=number of dates needed
#print(len(dates))

sessionID = 1
sessionDurations = [30,45,60,75,90,105,120,135,150,165,180]	# all in minutes
sessionStartTimes = 0
#"""

"""
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

for i in res:
	print(i)
"""
