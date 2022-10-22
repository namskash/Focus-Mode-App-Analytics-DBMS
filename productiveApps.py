from tkinter.ttk import Treeview,Style
import mysql.connector
from PIL import ImageTk
from tkinter import *
import sys
from time import sleep
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#import welcomePage

mydb = mysql.connector.connect(
	host="localhost",
	user="namskash",
	password="abcd",
	database="focusModeDBMS"
)

mycursor = mydb.cursor(buffered=True)

def productiveApps():
	global root
	root=Tk()
	root.title("Productive apps")
	root.geometry("1260x720")
	root.minsize(1260,720)
	root.state('zoomed')
	root.iconbitmap(r'images/logo.ico')

	#* Canvas:
	canvas1=Canvas(root,width=1260,height=720,border=0,bd=10,relief=SUNKEN,bg="#33cccc")
	img=ImageTk.PhotoImage(file="images/code2.png")
	canvas1.create_image(0,0,image=img,anchor=NW)

	#* Text:
	text1="| Productive Apps:"

	#? Approach 1: transparent text
	root.wm_attributes('-transparentcolor','#ab23ff')
	canvas1.create_text(80,50,text=text1,fill="#ffffff",font=("Georgia",40,"bold"),anchor=W)

	#button = [welcomePage.homeScreen]

	back_img = PhotoImage(file="images/back.png")
	backButton = Button(canvas1,image=back_img,borderwidth=0,highlightthickness = 0, bd = 0)
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

	apps=Treeview(canvas1,columns=(1,2,3,4,5),show="headings",height="5")	# Table 1
	apps.column(1,anchor=W,width=100)
	apps.column(2,anchor=W,width=100)
	apps.column(3,anchor=CENTER,width=100)
	apps.column(4,anchor=CENTER,width=100)
	apps.column(5,anchor=CENTER,width=100)
	apps.heading(1,text="appID")
	apps.heading(2,text="appName")
	apps.heading(3,text="timer")
	apps.heading(4,text="timerMAX")
	apps.heading(5,text="no. of times used")
	canvas1.update()						# Otherwise body width is taken to be 1 as the next func is called before body loads

	apps.place(relx = 0.05,rely = 0.15,relheight = 0.75,relwidth = 0.5)

	# Get appIDs and number of breaks the app was used in
	mycursor.execute("select appID,count(appID) from SESSION_APPS group by appID order by appID")
	temp = mycursor.fetchall()
	appIDs = []
	appBreakCount = []

	for i in temp:
		appIDs.append(i[0])
		appBreakCount.append(i[1])

	# Fill table
	index = 0
	mycursor.execute("select appID,appName,timer,timerMAX from APPS where privileged = 0x01")
	temp = mycursor.fetchall()
	for i in temp:
		apps.insert('','end',values=i + (appBreakCount[index],))
		index += 1
	
	#% Pie chart
	frame=LabelFrame(canvas1,text="Distribution:",font=("Century Gothic",18),fg="#ffffff",bg="#001a33",padx=10,pady=5,relief=SUNKEN,bd=5)
	frame.place(relx=0.6,rely=0.3,width=500,height=400)

	appList=[]
	appSplit=[]

	# Fill appSplit
	totalBreaks = sum(appBreakCount)
	for i in appBreakCount:
		appSplit.append(i / totalBreaks)

	# Fill appList
	for i in appIDs:
		vals = (i,)
		mycursor.execute("select appName from APPS where appID = %s",vals)
		temp = mycursor.fetchall()
		appList.append(temp[0][0])

	fig = Figure() # create a figure object
	ax = fig.add_subplot(111) # add an Axes to the figure
	ax.pie(appSplit, radius=1, labels=appList,autopct='%0.2f%%', shadow=True)

	chart = FigureCanvasTkAgg(fig,frame)
	chart.get_tk_widget().pack()

	canvas1.place(relwidth=1,relheight=1,relx=0,rely=0)
	root.mainloop()

productiveApps()
