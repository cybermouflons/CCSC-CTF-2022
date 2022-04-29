from Audio import *
import numpy as np
from scipy.io import wavfile
import socket
import struct



addr = ("0.0.0.0",9001)
s : socket.socket = socket.create_server(addr,family=socket.AF_INET)

random.seed(b"D4mn R1ck")
s.listen(1)

while True:
	conn, addr = s.accept()
	print (f"Established connection with {addr[0]}")
	conn.send(b"I hope that you understand Bird Language...Be quick!\n")
	try:
		conn.send(b"Are you ready [Y or N]?\n")
		while True:
			resp = conn.recv(0x1)
			if resp is not None:
				break
		if resp == b'Y':
			conn.settimeout(10.0)
			conn.send(b"The timer has started... Tik tok tok\n")
			
			#creates the wav file
			challenge = Audio("challenge.wav")
			conn.sendall(challenge.payload)
			response = b''
			length_data = conn.recv(0x4)
			length = struct.unpack("I",length_data)[0]
			while len(response) != length:
				response += conn.recv(4096)
			f = open("response.wav","wb")
			f.write(response)
			f.close()
			
			#process the wav file
			response_profiles = solver("response.wav")
			if ((response_profiles is not None) and len(response_profiles) == 2):
				if (response_profiles[0][0] == challenge.profile[0][0]) and (int(response_profiles[0][1]) == challenge.profile[0][1]) and (response_profiles[1][0] == challenge.profile[1][0]) and (int(response_profiles[1][1]) == challenge.profile[1][1]) :
					conn.send(b"Welcome to the Bird World. CCSC{y0u_e4rn3d_y0ur_w4y_t0_b1rd_w0rld!}\n")
				else:
					conn.send(b"Wrong Response\n")
			else:
				conn.send(b"Are you a member of Galactic Federation?? Because you do not know our language...\n")
		else:
			conn.send(b"Did you chicken out?\n")
		conn.close()
	except socket.timeout:
		conn.send(b"You are weak...\n")
		conn.close()

    



