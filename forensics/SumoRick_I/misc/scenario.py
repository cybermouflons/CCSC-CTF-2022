'''
SumoRick I
DIFFICULTY: Medium

Ricks from various dimensions tried to enter the multiverse. 
Unfortunately their Mortys had messed around with Ricks' portal guns, 
leading their Ricks to enter the spiderverse and get abducted by Gromflomite assasins.
To lose their track, they kept visiting different planets in the spiderverse.
However, Krombopulos Michael (the Gromflomite who abducted the Rick of our dimension),
was secretly leaving messages behind to help Morty find his Rick.
'''

'''
SumoRick II
DIFFICULTY: Hard

In another dimension (let's call it meta-dimension), 
Ricks from various (normal) dimensions have also tried to enter the multiverse and accidentally entered the spiderverse.

In this meta-dimension, the Gromflomite assasins are smarter.
To lose their track, they changed spaceships each time they were visiting another planet.

However, Krombopulos Michael (the Gromflomite who abducted the Rick of our dimension),
was once again secretly leaving messages behind to help Morty find his Rick.
'''
import random
import traci
import sys
import sumolib
net = sumolib.net.readNet('spiderverse.net.xml')
sumoBinary = "sumo"
sumoCmd = [sumoBinary, "-c", "spiderverse.sumocfg" , "--tripinfo-output", "output.xml"]

max_num = 9
min_num = 1
alphabet = "ABCDEFGHI_KLMNOP{RSTUVWXY}"
flag = "CCSC{FINDING_RICK_IS_NOT_AN_EASY_TASK}"

def random_text(length):
	global alphabet
	x = ""
	for j in range(0,length):
		i = random.randint(0,len(alphabet)-1)
		x += alphabet[i]
	if x.startswith("CCSC{"):
		x = x.replace("CCSC{","ABCD{")
	return x

def find_random(num):
	x = num
	global max_num
	global min_num
	while x == num:
		x = random.randint(min_num,max_num)
	return x

def create_path(text):
	num = -1
	new_text = []
	for x in text:
		node = ""
		node += x
		num = find_random(num) if x != "A" else 1
		node += str(num)
		new_text.append(node)
	return new_text
	
drivers = 200
paths = []
for i in range(drivers):
	text = create_path(random_text(len(flag)))
	paths.append(text)
paths.append(create_path(flag))
random.shuffle(paths)


def algorithm1():
	global paths, drivers, sumoCmd
	driver_car_map={}
	driver = 0
	car = 0
	sumoCmd[-1] = "output1.xml"
	traci.start(sumoCmd)
	for path in paths:
		driver_car_map[str(driver)]=[]
		for i in range(len(path)-1):
			from_road = net.getNode(path[i]).getOutgoing()[0].getID()
			to_road = net.getNode(path[i+1]).getIncoming()[0].getID()
			traci.route.add("trip"+str(car), [from_road, to_road])
			driver_car_map[str(driver)].append(str(car))
			car+=1
		driver+=1
		
	car = 0
	car_driver_map={}
	for driver in range(drivers):
		tripID = driver_car_map[str(driver)].pop(0)
		traci.vehicle.add("SpaceShip"+str(car), "trip"+tripID, depart = "0")
		car_driver_map[str(car)] = str(driver)
		car+=1
		
	while traci.simulation.getMinExpectedNumber() > 0:
		traci.simulationStep()
		arrived = traci.simulation.getArrivedIDList()
		for id in arrived:
			old_car = id.split("SpaceShip")[1]
			driver = car_driver_map[str(old_car)]
			vehs = driver_car_map[str(driver)]
			if len(vehs)>0:
				tripID = driver_car_map[str(driver)].pop(0)
				traci.vehicle.add("SpaceShip"+str(old_car), "trip"+tripID, depart = "now")
	
algorithm1()