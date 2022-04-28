from BitVector  import BitVector
import struct

#https://engineering.purdue.edu/kak/dist/BitVector-3.5.0.html
class Pack:
	
	def __init__(self, phrase, par, pos, cipher_pos, reference=None):
		self.phrase = phrase
		self.par = par
		self.pos = pos
		self.cipher_pos = cipher_pos
		self.reference = reference

		if reference is None:
			self.text = phrase.text
			self.bv1 = BitVector(size=8)
			self.bv2 = BitVector(size=8)
			self.bv3 = BitVector(size=8)
			self.parse12()
		else:
			self.text = reference.text
			self.bv1 = BitVector(size=8)
			self.bv2 = BitVector(size=8)
			self.parse34()
	
	def parse12(self,):
		self.bv3[3:8] = BitVector(intVal = self.phrase.__len__(),size = 5)
		if self.phrase.par == self.par and self.cipher_pos-self.phrase.cipher_pos <= 0x3ff:
			self.case1()
		else:
			self.case2()
	
	def parse34(self,):		
		if self.reference.par == self.par and self.cipher_pos - self.reference.cipher_pos <= 0x3ff:
			self.case3()
		else:
			self.case4()


		
	def case1(self,):
		self.bv1[:3] = BitVector(intVal = 4,size = 3)
		self.init_position(self.cipher_pos-self.phrase.cipher_pos)
		self.data = struct.pack("BBB",int(self.bv1),int(self.bv2),int(self.bv3))
		print (f"[*] Opcode 1: {int(self.bv1)} {int(self.bv2)} {int(self.bv3)} \t:O={int(self.bv1[:3])} P={int(self.bv1[3:6])} E={int(self.bv1[6:8])} X={int(self.bv2)} L={int(self.bv3)} \t:{self.phrase.text}: {self.par},{self.pos}")

	def case2(self,):
		self.bv1[:3] = BitVector(intVal = 5,size = 3)
		self.init_position(self.phrase.cipher_pos)
		self.bv1[3:6] = BitVector(intVal = self.phrase.par  ,size = 3) 
		self.data = struct.pack("BBB",int(self.bv1),int(self.bv2),int(self.bv3))
		print (f"[*] Opcode 2: {int(self.bv1)} {int(self.bv2)} {int(self.bv3)} \t:O={int(self.bv1[:3])} P={int(self.bv1[3:6])} E={int(self.bv1[6:8])} X={int(self.bv2)} L={int(self.bv3)} \t:{self.phrase.text}: {self.par},{self.pos}")

	def case3(self,):
		self.bv1[:3] = BitVector(intVal = 6,size = 3)
		self.init_position(self.cipher_pos - self.reference.cipher_pos)
		self.data = struct.pack("BB",int(self.bv1),int(self.bv2))
		print (f"[*] Opcode 3: {int(self.bv1)} {int(self.bv2)}  \t:O={int(self.bv1[:3])} {int(self.bv1[3:6])} E={int(self.bv1[6:8])} X={int(self.bv2)} \t:{self.reference.text}: {self.par},{self.pos}")


	def case4(self,):
		self.bv1[:3] = BitVector(intVal = 7,size = 3)
		self.init_position(self.reference.cipher_pos)
		self.bv1[3:6] = BitVector(intVal = self.reference.par  ,size = 3) 
		self.data = struct.pack("BB",int(self.bv1),int(self.bv2))
		print (f"[*] Opcode 4: {int(self.bv1)} {int(self.bv2)} \t:O={int(self.bv1[:3])} P={int(self.bv1[3:6])} E={int(self.bv1[6:8])} X={int(self.bv2)} \t:{self.reference.text}: {self.par},{self.pos}")


	def init_position(self, phrase_pos):
		if phrase_pos <= 0xff:
			self.bv2 = BitVector(intVal = phrase_pos, size = 8)
		elif phrase_pos <= 0x3ff:
			#the position is defined with 12 bits
			temp = BitVector(intVal = phrase_pos, size = 10)
			self.bv1[6:] = temp[:2]
			self.bv2 = temp[2:]
		else:
			print("ERROR on position byte:",phrase_pos)

	def __str__(self):
		return self.phrase.text
