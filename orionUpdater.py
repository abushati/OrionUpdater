import orionsdk
import os
from difflib import SequenceMatcher
import time
from tkinter import *	

orion = orionsdk.SwisClient("dotnpm02", "abushati","aug2018AB")
results = orion.query("SELECT IPAddress\
						FROM Orion.Nodes")

listOfIPOrion = []
notOnSW = []
listOfIPsCRT = []
inSW = []
IPtoDevice = {}
communityString = "netOP$RO"
nodeStatusPolling = "120 seconds"
collectStatEvery = "10 minutes"
pollingEngin = "DOTNPM02"
NodeCategory = "Auto-detected"
topologyPollingInterval = "30 minutes"
SNMPPort = "161" #allow 64 bit counter
SNMPversion = "3"


def post(IPtoDevice,notOnSW):
	for IPs in notOnSW:
		print(IPs + ":" + IPtoDevice.get(IPs))




secureCRTIPs = open("/Users/arvid/Desktop/ipAddesses.txt","r")

for lines in secureCRTIPs:
	if ":" not in lines:
		CRT = lines.strip()
	else:
		device = lines.split(":")[0].strip()
		deviceIP = lines.split(":")[1].strip()
		#print(deviceIP)
		fullName = CRT + ' ' + device
		#fullName = fullName.replace("-"," ").replace("_"," ").upper().replace("AVE"," ").replace("ST"," ").replace("TH"," ")
		#fullName = fullName.replace(" ","")
		IPtoDevice.update({deviceIP : fullName })
		#print(IPtoDevice)
		if CRT != "":
			listOfIPsCRT.append(deviceIP)
print (listOfIPsCRT)

for i in range(0,len(results["results"])):
	orionIP = results["results"][i]["IPAddress"]
	#print(orionIP)
	#orionIP = orionIP.split(".")[0].upper().strip()
	listOfIPOrion.append(orionIP)

print(listOfIPOrion)

for IPsCRT in listOfIPsCRT:
	counter = 0
	rating = .80
	if IPsCRT in listOfIPOrion:
		inSW.append(IPsCRT)
		#print(listOfIPOrion.index(IPsCRT))
		#print(IPsCRT)
		#print(listOfIPOrion[listOfIPOrion.index(IPsCRT)])
	else:	
		notOnSW.append(IPsCRT)

master = Tk()
scrollbar = Scrollbar(master)
scrollbar.pack( side = RIGHT, fill = Y )
mylist = Listbox(master, yscrollcommand = scrollbar.set )
mylist.config(width = 0)

master.geometry("600x600")
number = 0
for IPs in notOnSW:
	mylist.insert(END,(IPs,IPtoDevice.get(IPs)))
	#mylist.insert(END,IPtoDevice.get(IPs))
	mylist.pack(side = LEFT, fill = BOTH)

	scrollbar.config(command = mylist.yview)
button = Button(master, text = "SUBMIT",command= lambda: post(IPtoDevice,notOnSW))
button.pack()#.grid(row=3, column=3, sticky=W, pady=4)

mainloop()






















