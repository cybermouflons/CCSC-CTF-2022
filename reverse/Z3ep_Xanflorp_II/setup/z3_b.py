from random import random
import numpy as np
from z3 import *

import socket
import struct
'''
Shit Morty... The portal gun is still broken. You need to fix it Morty BURPPP. FIX IT!!!
Some weird shits are happening. Grandpa will have his alone time now. Fix the circuitboard till i'm back Morty.
'''
##### Set up server
addr = ("127.0.0.1",1235)
sock : socket.socket = socket.create_server(addr,family=socket.AF_INET)
sock.listen(1)
conn, addr = sock.accept()
print (f"Established connection with {addr[0]}")
conn.send(b"Let's see if you can fix my teleport gun Morty...\n")

try:
	##### Intro
	conn.send(b"Some weird equations will appear.\n")
	conn.send(b"Respond with floats, separated by space.\n")
	conn.send(b"You must be quick or else the portal gun's circuit will overheat!\n")
	conn.send(b"Are you ready [Y or N]?\n")
	while True:
		resp = conn.recv(1000)
		if resp == b'Y\n':
			break
	
	##### Set up constraints
	MAX_INT = 100
	GOAL = 50
	for times in range(GOAL):
		SIZE = 1#int(random()*10)+1
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
			message = str(eq).replace("\n","")+"\n"
			message = message.replace("+-","- ")
			message = message.replace("+","+ ")
			conn.send(bytes(message,"utf-8"))
		conn.send(bytes("Solution: \n","utf-8"))
		
		##### Receive response
		conn.settimeout(10.0)
		response = str(conn.recv(1000))
		conn.settimeout(0)
		response = response.replace("b\'","")[:-3].split(" ")
		try:
			reponse = [float(x) for x in response]
		except Exception:
			conn.send(b"Wrong format Morty, you broke it!\n")
			conn.close()
			sock.close()
			break
		
		##### Add response to the system
		for i in range(min(len(x),len(response))):
			s.add(x[i] == response[i])
		
		##### Check if sat
		if len(response) != len(x) or s.check() != sat:
			conn.send(b"Wrong answer Morty...Burrrrrp\n")
			conn.close()
			sock.close()
			break
	else:
		conn.send(b"Burrrrp Good job Morty! We can play Galactic Bingo now! Here's the flag:\n")
		conn.send(b"CCSC{C0n5tr41nt_S0lver5_Are_Fun!}\n")
		conn.close()
		sock.close()
		
except socket.timeout:
	conn.send(b"Time's up Morty...You burned it!\n")
	conn.close()
	sock.close()
	




