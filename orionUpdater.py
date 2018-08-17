import orionsdk
import os
from difflib import SequenceMatcher
import time
from tkinter import *	

orion = orionsdk.SwisClient("", "","")
results = orion.query("SELECT Caption,  DisplayName \
						FROM Orion.Nodes")

listOfNamesOrion = []
notOnSW = []
listOfNamesCRT = []
inSW = []
deviceToIp = {}

def checker(rating,counter,listOfNamesOrion,devicesCRT):
	tempList = []
	for names in listOfNamesOrion:
		if (SequenceMatcher("",devicesCRT,names).ratio() >=rating):
			tempList.append(names)
	print(devicesCRT,tempList)
	if len(tempList) == 1:
		
		master = Tk()
		master.geometry("500x200")
		Label(master, text = devicesCRT).grid(row=0)
		Button(master, text = tempList[0], command = lambda: inSW.append(tempList[0])).grid(row=3, column=0, sticky=W, pady=4)
		Button(master, text ="Quit", command = master.destroy).grid(row=3, column=1, sticky=W, pady=4)

		mainloop()
	elif tempList == []:
		print("nothing in this list")
	else:
		master = Tk()
		master.geometry("600x100")
		Label(master, text=devicesCRT).grid(row=0)
		

		e1 = Entry(master)
		e2 = Entry(master)
		num = 0 
		for i in range(0,len(tempList)):
			Button(master, text= tempList[i], command = lambda: inSW.append(tempList[i])).grid(row=3, column=num, sticky=W, pady=4)

		
			num += 1
		print(inSW)
		Button(master, text="Quit", command = master.destroy).grid(row=3, column=num, sticky=W, pady=4)
		print(inSW)
		mainloop()

def post(deviceToIp,notOnSW):
	for devices in notOnSW:
		print(devices + ":" + deviceToIp.get(devices))






	 
	


secureCRTnames = open("","r")

for lines in secureCRTnames:
	if ":" not in lines:
		CRTname = lines.strip()
	else:
		device = lines.split(":")[0].strip()
		deviceIP = lines.split(":")[1].strip()
		#print(deviceIP)
		fullName = CRTname + ' ' + device
		fullName = fullName.replace("-"," ").replace("_"," ").upper().replace("AVE"," ").replace("ST"," ").replace("TH"," ")
		fullName = fullName.replace(" ","")
		deviceToIp.update({fullName : deviceIP})
		print(deviceToIp)
		if CRTname != "":
			listOfNamesCRT.append(fullName)
#print (listOfNamesCRT)

for i in range(0,len(results["results"])):
	orionName = results["results"][i]["DisplayName"]
	orionName = orionName.split(".")[0].upper()
	orionName = orionName.replace("-"," ").replace("_"," ").replace("AVE"," ").replace("ST"," ").replace("TH"," ")
	orionName = orionName.replace(" ","")
	if orionName != " ":
		listOfNamesOrion.append(orionName)
#print(listOfNamesOrion)

for devicesCRT in listOfNamesCRT:
	counter = 0
	rating = .80
	if devicesCRT in listOfNamesOrion:
		inSW.append(devicesCRT)
		#print(listOfNamesOrion.index(devicesCRT))
		#print(devicesCRT)
		#print(listOfNamesOrion[listOfNamesOrion.index(devicesCRT)])
		listOfNamesOrion.remove(devicesCRT)
		listOfNamesCRT.remove(devicesCRT)
	else:	
		pass
		#checker(rating,counter,listOfNamesOrion,devicesCRT)
for remainingNamesCRT in (set(listOfNamesCRT) - set(inSW)):
	notOnSW.append(remainingNamesCRT)

master = Tk()
scrollbar = Scrollbar(master)
scrollbar.pack( side = RIGHT, fill = Y )
mylist = Listbox(master, yscrollcommand = scrollbar.set )
mylist.config(width = 0)

master.geometry("600x600")
number = 0
for items in notOnSW:
	mylist.insert(END,items)
	mylist.pack(side = LEFT, fill = BOTH)

	scrollbar.config(command = mylist.yview)
button = Button(master, text = "SUBMIT",command= lambda: post(deviceToIp,notOnSW))
button.pack()#.grid(row=3, column=3, sticky=W, pady=4)

mainloop()
