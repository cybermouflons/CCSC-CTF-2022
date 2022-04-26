from PIL import Image
from BitVector import BitVector
import sys

im = Image.open(sys.argv[1])

pixels = im.load()

width,height = im.size

flag = BitVector(size=0)

print ("Solution")

directions = 1
for h in range(4):
	if directions == 1:
		for w in range(0,width,2):
			d = pixels[w+1,h] - pixels[w,h]
			if (pixels[w,h]> 15 and pixels[w+1,h] > 15):
				if abs(d) in range(8,16):
					flag += BitVector(intVal = abs(d)-8,size=3)
				elif abs(d) in range(16,32):
					flag += BitVector(intVal = abs(d)-16,size=4)
		directions = -1
	else:
		for w in range(width-1,0,-2):
			d = pixels[w-1,h] - pixels[w,h]
			if (pixels[w,h]> 15 and pixels[w-1,h] > 15):
				if abs(d) in range(8,16):
					flag += BitVector(intVal = abs(d)-8,size=3)
				elif abs(d) in range(16,32):
					flag += BitVector(intVal = abs(d)-16,size=4)
		directions = 1
print (flag)
