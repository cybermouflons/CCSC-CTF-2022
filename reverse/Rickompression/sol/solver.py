from BitVector  import BitVector
import numpy as np
import struct

class Pack:
	def __init__(self,enc):
		codes = ''.join(format(i, '08b') for i in enc)

		self.opcode = int(codes[:3], 2)
		self.par = int(codes[3:6], 2)
		self.ext = int(codes[6:8], 2)
		self.pos = int(codes[8:16], 2)
		self.pad = int(codes[16:19], 2)
		self.leng = int(codes[19:24], 2)
		
		print(self.opcode,self.par,self.ext,self.pos,self.pad,self.leng)
		self.pos = int(codes[6:16], 2)
	

def decipher(ciphertext, cursor, par_pos, pack):
	opcode = pack.opcode
	par = pack.par
	pos = pack.pos
	leng = pack.leng
	text=""
	if opcode== 4:
		text = str(ciphertext[cursor-pos:cursor-pos+leng])[2:-1]
	elif opcode ==5:
		text = str(ciphertext[par_pos[par]+pos:par_pos[par]+pos+leng])[2:-1]
	elif opcode ==6:
		enc = ciphertext[cursor-pos:cursor-pos+3]
		print(enc)
		pack2 = Pack(enc)
		text = decipher(ciphertext, cursor-pos, par_pos, pack2)
	elif opcode ==7:
		enc = ciphertext[par_pos[par]+pos:par_pos[par]+pos+3]
		print(enc)
		pack2 = Pack(enc)
		text = decipher(ciphertext, par_pos[par]+pos, par_pos, pack2)

	print(":"+text+":")
	return text
	
## Open IO files
f1 = open("cipherrick.txt", "rb")
f2 = open("solution.txt", "w")
ciphertext = f1.read()

phrases = {}

par_pos = {}
par_pos[0]=0
decipher_text = ""

## Read all the input file by incrementing the cursor
cursor = -1
enc_par = 0
while cursor < len(ciphertext)-2:
	cursor +=1
	
	if ciphertext[cursor]<128:
		decipher_text += chr(ciphertext[cursor])
		if chr(ciphertext[cursor])=="\n":
			enc_par +=1	
			par_pos[enc_par] = cursor
			decipher_text+="\n"
		continue
		
	enc = bytearray(ciphertext[cursor:cursor+3])
	pack = Pack(enc)
	
	text = decipher(ciphertext, cursor, par_pos, pack)
	decipher_text+=text
	
	opcode = pack.opcode
	if opcode == 4 or opcode == 5:
		cursor += 2
	elif opcode == 6 or opcode == 7:
		cursor += 1
		


f2.write(decipher_text)	
f1.close()
f2.close()	
