import xml.etree.ElementTree as ET

tree = ET.parse('output2.tripinfo.xml')
root = tree.getroot()
infos = {}
ships = set()

# Finds the next possible spaceships recursively.
# It stores each route in the routes list
def findNext(id,route,routes):
	global infos,ships
	arr_time = infos[id]["arr_time"]
	# Add the departure character of this spaceship
	route += infos[id]["dep"]
	next_ships = []
	# Find the next possible spaceships
	for ship in ships:
		if arr_time <= infos[ship]["dep_time"] <= arr_time+5 and infos[id]["arr"]==infos[ship]["dep"]:
			next_ships.append(ship)
	# If it doesn't look like the flag, stop searching
	# Otherwise, check all next possibilities
	if len(route)==5 and route!="CCSC{":
		return 
	for next_ship in next_ships:
		findNext(next_ship, route, routes)
		
	# If there are no next possibilites, add the arrival character to route and add to list
	if len(next_ships)==0:
		route += infos[id]["arr"]
		if route[-1] == "}":
			routes.append(route)

#Put together the departures and arrivals
for child in root:
	id = child.attrib["id"]
	ships.add(id)
	info ={}
	info["dep"] = child.attrib["departLane"][0] #First character
	info["arr"] = child.attrib["arrivalLane"][2] #Third character
	info["dep_time"] = float(child.attrib["depart"])
	info["arr_time"] = float(child.attrib["arrival"])
	infos[id]= info

#Begin searching only for spaceships that departed on time 0.	
routes = []
for ship in ships:
	if infos[ship]["dep_time"]==0:
		findNext(ship,"", routes)
		print("----------------")
		
for route in routes:
	print(route)