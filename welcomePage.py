import mysql.connector
from tkinter import *
from PIL import ImageTk,Image
from functools import partial
import sys
from time import sleep
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def clicked(num):
	global button_id
	button_id = num+1
	global buttons

	sleep(0.1)
	
	root.destroy()
	#buttons[button_id].invoke()

#When the mouse hovers over one of the button
def enter(i, event):
	buttons[i]['fg'] = "white"

def leave(i, event):
	buttons[i]['fg'] = "#112233"

def roles(emp_id):
	#print(emp_id)
	global root
	root=Tk()
	root.title("Welcome!")
	root.geometry("1260x720")
	root.minsize(1260,720)
	root.state('zoomed')

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
	canvas1.create_text(130,190,text=text2,fill="#ffffff",font=("Georgia",20),anchor=W)
	canvas1.create_text(900,190,text=text3,fill="#ffffff",font=("Georgia",20),anchor=W)

	"""
	# Approach 2: Non-transparent text
	frame1=LabelFrame(canvas1,width=500,padx=10,pady=10)
	Label1=Label(frame,text=text1,font=("Georgia",40,"bold"),fg="#112233",bg="#00b3b3")
	Label2=Label(frame,text=text2,font=("Georgia",20),fg="#112233",bg="#00b3b3")
	Label1.grid(row=0,column=0)
	Label2.grid(row=1,column=0)
	frame1.place(relx=0.1,rely=0.1)
	"""

	#* Roles:
	no_of_projects=4	# table #2 check how many are null and sub from 4
	y=0.15
	backgrounds=["#00ff00","#00ffff","#ff1a75","#ffff00"]
	backgrounds_active=["#004d00","#004d4d","#660029","#4d4d00"]
	functions=["Past sessions","Most used apps","","Timers"]  # I/P From table #3

	## role 1:
	global buttons
	buttons=[]

	global button_id
	button_id=1

	for i in range(no_of_projects):
		frame=LabelFrame(canvas1,bg="#001a33",padx=10,pady=5,relief=SUNKEN,bd=5)
		button_text="Project %d"%(i+1)
		button=Button(frame,text=button_text,font=("Georgia",20,"bold"),fg="#112233",bg=backgrounds[i],activebackground=backgrounds_active[i],activeforeground="#cccccc",
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
	frame=LabelFrame(canvas1,text="At a glance:",font=("Century Gothic",10),fg="#ffffff",bg="#001a33",padx=10,pady=5,relief=SUNKEN,bd=5)
	frame.place(relx=0.6,rely=0.3,width=500,height=400)

	appList=['Chrome','Prime Video','YouTube','Word','VS Code']
	appSplit=[12,35,40,10,10]

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

roles(1104)