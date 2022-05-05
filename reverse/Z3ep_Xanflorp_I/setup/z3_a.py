from random import random
import numpy as np
from z3 import *
#import socket
#import struct

##### Set up server
#addr = ("127.0.0.1",1234)
#sock : socket.socket = socket.create_server(addr,family=socket.AF_INET)
#sock.listen(1)
#conn, addr = sock.accept()
#print (f"Established connection with {addr[0]}")
print("Those Gromflomites... We must destroy their DNA.")

##### Intro
print("Did you find the parameters of the dissolving protein?\nWrite the parameters as floats, separated by space. XY.")

##### Set up constraints
SIZE = 3
x = RealVector('x', SIZE)
y = RealVector('y',SIZE)

c11 , c12, c13 = 5,2,3
c21 , c22, c23 = 4,5,6
c31 , c32, c33 = 7,8,5

eq1 = c11*x[0] + c12*x[1] + c13*x[2] - y[0] + y[1] - y[2] == x[0]
eq2 = c21*x[0] + c22*x[1] + c23*x[2] + y[0] - y[1] - y[2] == x[1]
eq3 = c31*x[0] + c32*x[1] + c33*x[2] + y[0] + y[1] + y[2] == x[2]
eq4 = x[0] < -4
eq5 = x[1] > 7
eq6 = x[1] + x[2] == 3
eq7 = x[0] != x[2]

s = Solver()
s.add(eq1,eq2,eq3, eq4, eq5,eq6, eq7)
#print(eq1,eq2,eq3, eq4, eq5,eq6, eq7)
#print(s.check())
#print(s.model())
	
##### Receive response
response = input()
response = response.split(" ")
try:
	reponse = [float(x) for x in response]
	if len(response) != SIZE*2 :
		raise Exception("")
except Exception:
	print("Wrong format Morty, you doomed us all!")
	#conn.close()
	#sock.close()
	exit(0)

##### Add response to the system
for i in range(SIZE):
	s.add(x[i] == response[i])
for i in range(SIZE,SIZE*2):
	s.add(y[i-SIZE] == response[i])
#print(response)

##### Check if sat
if s.check() != sat:
	print("Wrong answer Morty...Burrrrrp")
	#conn.close()
	#sock.close()
else:
	print("Burrrrp Good job Morty! You deserve a trip to Blips and Chitz!\nHere's the flag to enter:")
	print("CCSC{C0n5tr41nt_S0lver5_Are_Fun!}")
	#conn.close()
	#sock.close()