import xml.etree.ElementTree as ET

tree = ET.parse('output1.tripinfo.xml')
root = tree.getroot()
departures = {}
arrivals = {}
ships = set()
for child in root:
	id = child.attrib["id"]
	if id not in ships:
		ships.add(id)
		departures[id]=[]
		arrivals[id]=[]
	departures[id].append(child.attrib["departLane"][0])
	arrivals[id].append(child.attrib["arrivalLane"][-2])

sentences = []
for ship in ships:
	departures[ship].append(arrivals[ship][-1])
	sentences.append("".join(x for x in departures[ship]))
	
for sentence in sentences:
	if sentence.startswith("CCSC"):
		print(sentence)