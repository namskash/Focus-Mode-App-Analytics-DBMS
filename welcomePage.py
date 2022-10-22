from turtle import bgcolor
import mysql.connector
from tkinter import *
from PIL import ImageTk
from functools import partial
import sys
from time import sleep
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
"""
import pastSessions
import productiveApps
import unproductiveApps
import timers
"""

mydb = mysql.connector.connect(
	host="localhost",
	user="namskash",
	password="abcd",
	database="focusModeDBMS"
)

mycursor = mydb.cursor(buffered=True)

def clicked(num):
	global button_id
	button_id = num+1
	global buttons

	sleep(0.05)
	root.destroy()
	#buttons[button_id].invoke()

# When the mouse hovers over one of the buttons:
def enter(i, event):
	buttons[i]['fg'] = "white"

def leave(i, event):
	buttons[i]['fg'] = "#112233"

def homeScreen():
	global root
	root=Tk()
	root.title("Focus sessions")
	root.geometry("1260x720")
	root.minsize(1260,720)
	root.state('zoomed')
	root.iconbitmap(r'images/logo.ico')

	#* Canvas:
	canvas1=Canvas(root,width=1260,height=720,border=0,bd=10,relief=SUNKEN,bg="#33cccc")
	img=ImageTk.PhotoImage(file="images/code2.png")
	canvas1.create_image(0,0,image=img,anchor=NW)

	#* Text:
	name="Naman Kashyap"									# I/P from database -> table #2 -> emp_id -> emp_name
	text1=f"Welcome {name}!\n"
	text2=" Here are your stats:"
	text3="Your last session:"

	#? Approach 1: transparent text
	root.wm_attributes('-transparentcolor','#ab23ff')
	canvas1.create_text(130,150,text=text1,fill="#ffffff",font=("Georgia",40,"bold"),anchor=W)
	canvas1.create_text(130,190,text=text2,fill="#00ff99",font=("Georgia",20),anchor=W)
	canvas1.create_text(900,190,text=text3,fill="#00ff99",font=("Georgia",20),anchor=W)

	#* Buttons:
	no_of_projects=4	# table #2 check how many are null and sub from 4
	y=0.15
	backgrounds=["#00ff00","#00ffff","#ff1a75","#ffff00"]
	backgrounds_active=["#004d00","#004d4d","#660029","#4d4d00"]
	functions=["View past sessions","View most productive apps","Unproductive app-o-meter","View/update all timers"]  # I/P From table #3
	buttonNames = ["Sessions","Productive","Break-apps","Timers"]
	global buttons
	buttons = []	# [pastSessions.pastSessions, productiveApps.productiveApps,unproductiveApps.unproductiveApps,timers.timers]

	global button_id
	button_id=1

	for i in range(no_of_projects):
		frame=LabelFrame(canvas1,bg="#001a33",padx=10,pady=5,relief=SUNKEN,bd=5)
		button=Button(frame,text=buttonNames[i],font=("Georgia",18,"bold"),fg="#112233",bg=backgrounds[i],activebackground=backgrounds_active[i],activeforeground="#cccccc",
			width=10,borderwidth=15,command=partial(clicked,i))
		buttons.append(button)
		button.bind("<Enter>",partial(enter,i))
		button.bind("<Leave>",partial(leave,i))
		button.grid(row=0,column=0)
		project=Label(frame,text=": "+functions[i],font=("Century Gothic",20),padx=10,bg="#001a33",fg="white")
		project.grid(row=0,column=1)
		y+=0.15
		frame.place(relx=0.10,rely=y,width=700)
		#print(buttons)


	#% Pie chart
	frame=LabelFrame(canvas1,text="At a glance:",font=("Century Gothic",18),fg="#ffffff",bg="#001a33",padx=10,pady=5,relief=SUNKEN,bd=5)
	frame.place(relx=0.6,rely=0.3,width=500,height=400)

	appList=[]
	appSplit=[]

	mycursor.execute("select sessionID, duration from SESSIONS where sessionDate in(select max(sessionDate) from SESSIONS)")
	temp=mycursor.fetchall()
	sessionID, sessionDuration=temp[0][0],int(temp[0][1])

	# % APPS used in session:
	vals = (sessionID,)
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

	fig = Figure() # create a figure object
	ax = fig.add_subplot(111) # add an Axes to the figure
	ax.pie(appSplit, radius=1, labels=appList,autopct='%0.2f%%', shadow=True)

	chart = FigureCanvasTkAgg(fig,frame)
	chart.get_tk_widget().pack()

	canvas1.place(relwidth=1,relheight=1,relx=0,rely=0)
	root.mainloop()
	
	try:
		return button_id
	except:
		sys.exit()

homeScreen()
