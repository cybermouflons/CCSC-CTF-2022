from pwn import *
from Audio import *

#context.log_level = 'DEBUG'
r = remote("0.0.0.0",9001)

r.recvline()
r.recvline()
#r.recvline()

#Answer
r.send(b'Y')
r.recvline()

length_bytes = r.recv(0x4)
length = struct.unpack("I",length_bytes)[0]


challenge = b''

while len(challenge) != length:
	challenge += r.recv(4096)


f = open("challenge.wav","wb")
f.write(challenge)
f.close()

profiles = solver("challenge.wav")
response = Audio("response.wav",profiles)


r.send(response.payload)
r.interactive()

