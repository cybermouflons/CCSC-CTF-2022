from pwn import *
import struct

context.log_level = 'DEBUG'

r = remote("0.0.0.0",10002)
key = [97,79,23,54,85,75,38,114]
sol = b''

for k in key:
	sol += struct.pack("B",k)

r.send(sol)

r.interactive()
