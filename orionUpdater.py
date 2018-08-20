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


nodeidTOip = {}



def pushToSW(IPtoDevice,notOnSW):

	for Ips in notOnSW:
	# fill these in for the node you want to add!
		ip_address = Ips
		community = 'netOP$RO'

		# set up property bag for the new node
		props = {
		    'IPAddress': ip_address,
		    'EngineID': 1,
		    'ObjectSubType': 'SNMP',
		    'SNMPVersion': 2,
		    'Community': community,

		    'DNS': '',
		    'SysName': ''
		    }

		print("Adding node {}... ".format(props['IPAddress']), end="")
		results = orion.create('Orion.Nodes', **props)
		print(results)
		print("DONE!")


		# extract the nodeID from the result
		nodeid = re.search(r'(\d+)$', results).group(0)

		#ipsToNodeID.update({Ips : nodeid})

		pollers_enabled = {
		    'N.Status.ICMP.Native': True,
		    'N.Status.SNMP.Native': False,
		    'N.ResponseTime.ICMP.Native': True,
		    'N.ResponseTime.SNMP.Native': False,
		    'N.Details.SNMP.Generic': True,
		    'N.Uptime.SNMP.Generic': True,
		    'N.Cpu.SNMP.HrProcessorLoad': True,
		    'N.Memory.SNMP.NetSnmpReal': True,
		    'N.AssetInventory.Snmp.Generic': True,
		    'N.Topology_Layer3.SNMP.ipNetToMedia': False,
		    'N.Routing.SNMP.Ipv4CidrRoutingTable': False
			}

		pollers = []
		for k in pollers_enabled:
		    pollers.append(
		        {
		            'PollerType': k,
		            'NetObject': 'N:' + nodeid,
		            'NetObjectType': 'N',
		            'NetObjectID': nodeid,
		            'Enabled': pollers_enabled[k]
		        }
		    )

		for poller in pollers:
		    print("  Adding poller type: {} with status {}... ".format(poller['PollerType'], poller['Enabled']), end="")
		    response = orion.create('Orion.Pollers', **poller)
		    print("DONE!")

	#findInterface(ipsToNodeID,notOnSW)

	



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
label = Label(master, text = "These are the devices that are not on SolarWinds, \n to add them press submit")
label.pack(side = TOP)
for IPs in notOnSW:
	mylist.insert(END,(IPs,IPtoDevice.get(IPs)))
	#mylist.insert(END,IPtoDevice.get(IPs))
	mylist.pack(side = LEFT, fill = BOTH)

	scrollbar.config(command = mylist.yview)
button = Button(master, text = "SUBMIT",command= lambda: pushToSW(IPtoDevice,notOnSW))#pushToSW(IPtoDevice,notOnSW),fg = "blue")
button.pack()#.grid(row=3, column=3, sticky=W, pady=4)

mainloop()






















