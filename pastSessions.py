from tkinter.ttk import Treeview,Style
import mysql.connector
from PIL import ImageTk
from tkinter import *
import matplotlib.pyplot as plt
import numpy as np

import welcomePage

mydb = mysql.connector.connect(
	host="localhost",
	user="namskash",
	password="abcd",
	database="focusModeDBMS"
)

mycursor = mydb.cursor(buffered=True)

def home():
	global root
	root.destroy()
	welcomePage.homeScreen()

def ScrollAll(event):
	global canvas1
	canvas1.config(scrollregion=canvas1.bbox('all'), width=1000, height=1000)

def pie(event):
	global session
	selected = session.item(session.selection()[0])["values"]
	# of the form: (sessionID,date,startTime,endTime,duration,efficiency)

	appList=[]
	appSplit=[]

	vals = (selected[0],)
	mycursor.execute("select duration from SESSIONS where sessionID = %s",vals)
	temp=mycursor.fetchall()
	sessionDuration=int(temp[0][0])

	# % APPS used in session:
	vals = (selected[0],)
	mycursor.execute("select appName from APPS where appID in (select appID from SESSION_APPS where sessionID = %s )",vals)
	temp = mycursor.fetchall()
	for apps in temp:
		appList.append(apps[0])

	# % Number of focus apps
	index = len(appList)

	# % APPS used in all the breaks in session:
	mycursor.execute("select appName from APPS where appID in (select appID from BREAK_APPS where breakID in (select breakID from BREAKS where sessionID = %s ))",vals)	# vals = sessionID
	temp = mycursor.fetchall()
	for apps in temp:
		appList.append(apps[0])

	# % breakTime
	mycursor.execute("select breakDuration from BREAKS where sessionID = %s",vals)
	temp = mycursor.fetchall()
	breakDuration = int(temp[0][0])

	sessionDuration -= breakDuration				# sessionTime = sessionTime - breakTime
	sessionSplit = sessionDuration / index			# Just to divide the session pie into equal parts
	breakSplit = breakDuration / (len(appList) - index)
	thresh = 0.5

	for i in appList[:index]:
		appSplit.append(sessionSplit + thresh)
		thresh = thresh * -1
	for i in appList[index:]:
		appSplit.append(breakSplit + thresh)
		thresh = thresh * -1

	plt.pie(np.array(appSplit),labels=appList)
	plt.show()

def pastSessions():
	global root
	root=Tk()
	root.title("Past sessions")
	root.geometry("1260x720")
	root.minsize(1260,720)
	root.state('zoomed')
	root.iconbitmap(r'images/logo.ico')

	#* Canvas:
	global canvas1
	canvas1=Canvas(root,width=1260,height=720,border=0,bd=10,relief=SUNKEN,bg="#33cccc")
	img=ImageTk.PhotoImage(file="images/code2.png")
	canvas1.create_image(0,0,image=img,anchor=NW)

	#* Text:
	text1="| Past sessions:"
	text2="Double click to generate a pie chart"

	root.wm_attributes('-transparentcolor','#ab23ff')
	canvas1.create_text(80,50,text=text1,fill="#ffffff",font=("Georgia",40,"bold"),anchor=W)
	canvas1.create_text(115,90,text=text2,fill="#ffffff",font=("Century Gothic",15,"italic"),anchor=W)

	back_img = PhotoImage(file="images/back.png")
	backButton = Button(canvas1,image=back_img,borderwidth=0,highlightthickness = 0, bd = 0,command = home)
	backButton.place(relx=0.01,rely=0.035)

	style=Style()
	style.theme_use("clam")

	style.configure(
		'Treeview',
		background = "#edffb3",
		foreground = "#000000",
		fieldbackground = "#edffb3"
	)
	style.map('Treeview',
		background = [("selected","#e0ff33")],
		foreground = [("selected","#000000")]
	)
	style.configure(
		'Treeview.Heading',
		background = "#bfff00",
		foreground = "#000000",
		borderwidth = 0
	)

	global session
	session=Treeview(canvas1,columns=(1,2,3,4,5,6),show="headings",height="5")	# Table 1
	session.column(1,anchor=CENTER,width=100)
	session.column(2,anchor=CENTER,width=100)
	session.column(3,anchor=CENTER,width=100)
	session.column(4,anchor=CENTER,width=100)
	session.column(5,anchor=CENTER,width=100)
	session.column(6,anchor=CENTER,width=100)
	session.heading(1,text="sessionID")
	session.heading(2,text="Date")
	session.heading(3,text="Start time")
	session.heading(4,text="End Time")
	session.heading(5,text="Duration")
	session.heading(6,text="Efficiency")
	canvas1.update()						# Otherwise body width is taken to be 1 as the next func is called before body loads

	session.place(relx = 0.05,rely = 0.15,relheight = 0.75,relwidth = 0.9)

	#% Pie chart
	session.bind("<Double-1>",pie)

	# Fill into table
	query = """
		select s.*, round (duration / (duration + sum(breakDuration)), 3)
		from SESSIONS s join BREAKS b
		where s.sessionID = b.sessionID group by b.sessionID """
	mycursor.execute(query)
	temp = mycursor.fetchall()
	for i in range(len(temp)):
		session.insert('','end',values=temp[i])
	
	canvas1.place(relwidth=1,relheight=1,relx=0,rely=0)
	root.mainloop()

# pastSessions()
