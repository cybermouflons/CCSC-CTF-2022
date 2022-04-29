from random import random
import numpy as np
from z3 import *
import time
from inputimeout import inputimeout, TimeoutOccurred


#import socket
#import struct

##### Set up server
#addr = ("127.0.0.1",1235)
#sock : socket.socket = socket.create_server(addr,family=socket.AF_INET)
#sock.listen(1)
#conn, addr = sock.accept()
#print (f"Established connection with {addr[0]}")
print("Let's see if you can fix my teleport gun Morty...")
try:
	##### Intro
	print("Some weird equations will appear.")
	print("Respond with floats, separated by space.")
	print("You must be quick or else the portal gun's circuit will overheat!")
	print("Are you ready [Y or N]?")
	while True:
		resp = input()
		if resp == 'Y':
			break
	
	##### Set up constraints
	MAX_INT = 100
	GOAL = 50
	for times in range(GOAL):
		SIZE = int(random()*10)+1
		x = RealVector('x', SIZE)
		eqs = []
		for i in range(SIZE):
			c = np.random.uniform(-MAX_INT, MAX_INT, SIZE)
			eq = ""
			choice = random()
			if choice < 1./2:
				eq = simplify(np.sum([int(c[i])*x[i] for i in range(SIZE)])) <= int(random()*MAX_INT)
			else:
				eq = simplify(np.sum([int(c[i])*x[i] for i in range(SIZE)])) >= int(random()*MAX_INT)
			eqs.append(eq)
		
		##### Ignore unsolvable systems
		s = Solver()
		s.add(eqs)
		if s.check() != sat:
			GOAL +=1
			continue
		
		##### Send equations
		for eq in eqs:	
			message = str(eq).replace("\n","")
			message = message.replace("+-","- ")
			message = message.replace("+","+ ")
			print(message)
			
		##### Receive response
		try:
			response = inputimeout(prompt='Answer: ', timeout=10)
		except Exception:
			raise TimeoutOccurred
		response = response.split(" ")
		try:
			reponse = [float(x) for x in response]
		except Exception:
			print("Wrong format Morty, you broke it!")
			break
		
		##### Add response to the system
		for i in range(min(len(x),len(response))):
			s.add(x[i] == response[i])
		
		##### Check if sat
		if len(response) != len(x) or s.check() != sat:
			print("Wrong answer Morty...Burrrrrp")
			break
	else:
		print("Burrrrp Good job Morty! We can play Galactic Bingo now! Here's the flag:")
		print("CCSC{Y0u_w0uld_h4v3_n3v3r_b3li3v3d_th4t_c0nstr4int_s0lv3rs_4r3_s0_gr8}")
		
except TimeoutOccurred:
	print("Time's up Morty...You burned it!")



