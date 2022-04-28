class Phrase:
	min = 3
	max = 31
	
	def __init__(self, text, par, cipher_pos):
		self.text = text
		self.par = par
		self.cipher_pos = cipher_pos
		
	def __len__(self):
		return len(self.text)
		
	def __repr__(self):
		return self.text + " " + str(self.par) + " "+ str(self.cipher_pos)
		
	def __str__(self):
		return self.text
				
	def __lt__(self,phrase):
		return self.text.__lt__(phrase.text)
				
	def __eq__(self,phrase):
		return self.text.__eq__(phrase.text)
