import xml.etree.ElementTree as ET

tree = ET.parse('output1.tripinfo.xml')
root = tree.getroot()
departures = {}
arrivals = {}
ships = set()

#Find the departures and arrivals of each spaceship
for child in root:
	id = child.attrib["id"]
	if id not in ships:
		ships.add(id)
		departures[id]=[]
		arrivals[id]=[]
	departures[id].append(child.attrib["departLane"][0]) #First character
	arrivals[id].append(child.attrib["arrivalLane"][2]) #Third character

#Trace the route for each spaceship by 
# joining the departures' characters and 
# adding the last arrival character.
routes = {}
for ship in ships:
	departures[ship].append(arrivals[ship][-1])
	routes[ship]=("".join(x for x in departures[ship]))
	
#Find the route that begins with CCSC
for ship in ships:
	if routes[ship].startswith("CCSC"):
		print(ship,":",routes[ship])