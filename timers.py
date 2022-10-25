from tkinter.ttk import Treeview,Style
from turtle import update
import mysql.connector
from PIL import ImageTk
from tkinter import messagebox
from tkinter import *
from functools import partial

#import welcomePage

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
	#welcomePage.homeScreen()

def update(appIDentry,timer,timerMAX):
	if timerMAX < timer:
		messagebox.showwarning("Error!","timerMAX value must be greater than timer!")
		return
	
	vals = (appIDentry,)
	mycursor.execute("select appID from APPS where appID = %s and privileged = 0x00",vals)
	temp = mycursor.fetchall()

	if len(temp) == 0:
		messagebox.showerror("Error!","Invalid appID!")
		return
	else:
		messagebox.showinfo("Success!!","Timers updated for appID: %s"%appIDentry)

	try:
		mycursor.execute("update APPS set timer = %s, timerMAX = %s where appID = %s",(timer,timerMAX,appIDentry))
	except Exception as e:
		messagebox.showerror("Error!",e)
	# mydb.commit()

def timers():
	global root
	root=Tk()
	root.title("Timers")
	root.geometry("1260x720")
	root.minsize(1260,720)
	root.state('zoomed')
	root.iconbitmap(r'images/logo.ico')

	#* Canvas:
	canvas1=Canvas(root,width=1260,height=720,border=0,bd=10,relief=SUNKEN,bg="#33cccc")
	img=ImageTk.PhotoImage(file="images/code2.png")
	canvas1.create_image(0,0,image=img,anchor=NW)

	#* Text:
	text1="| Timers:"

	root.wm_attributes('-transparentcolor','#ab23ff')
	canvas1.create_text(80,50,text=text1,fill="#ffffff",font=("Georgia",40,"bold"),anchor=W)

	back_img = PhotoImage(file="images/back.png")
	backButton = Button(canvas1,image=back_img,borderwidth=0,highlightthickness = 0, bd = 0,command = home)
	backButton.place(relx=0.013,rely=0.036)


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

	appTimers=Treeview(canvas1,columns=(1,2,3,4),show="headings",height="5")	# Table 1
	appTimers.column(1,anchor=CENTER,width=100)
	appTimers.column(2,anchor=CENTER,width=100)
	appTimers.column(3,anchor=CENTER,width=100)
	appTimers.column(4,anchor=CENTER,width=100)
	appTimers.heading(1,text="appID")
	appTimers.heading(2,text="appName")
	appTimers.heading(3,text="timer")
	appTimers.heading(4,text="timerMAX")
	canvas1.update()						# Otherwise body width is taken to be 1 as the next func is called before body loads

	appTimers.place(relx = 0.05,rely = 0.15,relheight = 0.45,relwidth = 0.9)

	# Fill table
	index = 0
	mycursor.execute("select appID,appName,timer,timerMAX from APPS where privileged = 0x00")
	temp = mycursor.fetchall()
	for i in temp:
		appTimers.insert('','end',values=i)
		index += 1
	
	canvas1.place(relwidth=1,relheight=1,relx=0,rely=0)

	# Update frame:
	updateFrame = LabelFrame(canvas1,text = " Update timer:",font = ("Century Gothic",15,"italic"),bg = "#edffb3",fg="#000000",borderwidth=0)
	
	timerOptions = [
		"30 mins",
		"45 mins",
		"60 mins"
	]
	timer = StringVar()
	timer.set(timerOptions[0])
	timerMAX = StringVar()
	timerMAX.set(timerOptions[0])

	"""
	# auto select
	selected = appTimers.selection()
	if len(selected) == 1:
		appID.set(appTimers.item(selected)["appID"])
		timer.set(appTimers.item(selected)["timer"])
		timerMAX.set(appTimers.item(selected)["timerMAX"])
	"""

	# appID
	Label(updateFrame,text = "Enter appID: ",font = ("Century Gothic",10),bg = "#edffb3",fg="#000000",borderwidth=0).place(relx = 0.02,rely = 0.23)
	appIDentry = Entry(updateFrame,width = 6,font = ("Century Gothic",15),fg="#112233")
	appIDentry.place(relwidth = 0.06,relheight = 0.2,relx = 0.1, rely = 0.2)
	appIDentry.focus_set()	#put cursor in appIDentry
	
	# timer
	Label(updateFrame,text = "Enter new timer value: ",font = ("Century Gothic",10),bg = "#edffb3",fg="#000000",borderwidth=0).place(relx = 0.2,rely = 0.23)
	timerEntry = OptionMenu(updateFrame,timer,*timerOptions)
	timerEntry.place(relwidth = 0.06,relheight = 0.2,relx = 0.32, rely = 0.2)
	
	# timerMAX
	Label(updateFrame,text = "Enter new timerMAX value: ",font = ("Century Gothic",10),bg = "#edffb3",fg="#000000",borderwidth=0).place(relx = 0.4,rely = 0.23)
	timerMAXEntry = OptionMenu(updateFrame,timerMAX,*timerOptions)
	timerMAXEntry.place(relwidth = 0.06,relheight = 0.2,relx = 0.54, rely = 0.2)

	# Update button
	button=Button(updateFrame,text="Update",font=("Century Gothic",10),fg="#112233",bg="#00ff00",activebackground="#004d00",activeforeground="#cccccc",borderwidth=7,command = lambda : update(appIDentry.get(),timer.get(),timerMAX.get()))
	button.place(relx = 0.93,rely = 0.6,relheight=0.25)
	
	# Enter clicks the button:
	appIDentry.bind("<Return>", lambda event: update(appIDentry.get(),timer.get(),timerMAX.get()))
	timerMAXEntry.bind("<Return>", lambda event: update(appIDentry.get(),timer.get(),timerMAX.get()))
	timerEntry.bind("<Return>", lambda event: update(appIDentry.get(),timer.get(),timerMAX.get()))
	
	updateFrame.place(relx = 0.05,rely = 0.65,relheight=0.2,relwidth=0.9)

	root.mainloop()

# timers()
