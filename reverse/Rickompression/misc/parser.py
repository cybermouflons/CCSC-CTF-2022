from Phrase import Phrase
from Pack import Pack
import bisect
import struct

def BinarySearch(a, x):
	i = bisect.bisect_left(a, x)
	if i != len(a) and a[i] == x:
		return i
	else:
		return -1

## Open IO files
f1 = open("ricksum.txt", "r")
f2 = open("cipherrick.txt", "wb")
plaintext = f1.read()
cipher_text = bytearray()

## Init positional variables (par and pos) and hashmap for phrases.
par = 0
pos = -1
phrases = {}
packed_phrases = {}
for j in range(Phrase.max,Phrase.min-1,-1):
	phrases[j]=[]

## Read all the input file by incrementing the cursor
cursor = -1
cipher_pos = 0
count_packs =0
while cursor < len(plaintext)-2:
	cursor +=1
	pos+=1
	## New paragraph
	if plaintext[cursor]==plaintext[cursor+1]=="\n":
		par += 1
		pos = -1
		cipher_pos = 0
		continue
	## Sliding window to search for reoccurences
	for j in range(Phrase.max,Phrase.min-1,-1):
		text = plaintext[cursor:cursor + j]
		if "\n" in text:
			continue
		phrase = Phrase(text,par,cipher_pos)
		i = BinarySearch(phrases[j], phrase) ## NOTE: This brings the first occurence of the text.
		bisect.insort(phrases[j],phrase)
		#PACK phrase
		max_i = i
		while len(phrases[j]) > max_i+1 and phrases[j][max_i+1].text == phrases[j][i].text:
			max_i +=1
		
		if i>=0 :
			## Check if phrase in ciphertext is as expected (might include packed-bytes now)
			for i in range(i,max_i+1):
				phrase_in_cipher_text = "".join([chr(x) for x in cipher_text])[phrases[j][i].cipher_pos:phrases[j][i].cipher_pos+len(phrases[j][i])]
				if phrase_in_cipher_text == text:
					break
			else:
				continue
				
			if text not in packed_phrases:
				pack = Pack(phrases[j][i],par, pos, cipher_pos) #Cases 1,2
				cipher_pos += 3
			else:
				pack = Pack(None, par, pos, cipher_pos, packed_phrases[text]) #Cases 3,4
				cipher_pos += 2

			packed_phrases[text] = pack	#Updated packed_phrases
			cipher_text += pack.data
			
			cursor += len(phrases[j][i])-1
			pos += len(phrases[j][i])-1
			count_packs+=1
			break
		else:
			continue
	else: 
		## Python has For-Else. It executes when the for loop ends properly (does NOT break)
		cipher_text += str.encode(plaintext[cursor])
		#f2.write(str.encode(plaintext[cursor]))	
		cipher_pos += 1
		
print(count_packs)
f2.write(cipher_text)		
f1.close()
f2.close()	
