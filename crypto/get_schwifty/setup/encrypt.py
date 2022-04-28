from Crypto.Cipher import DES
import base64
import random

keys=["0000000000000000","FFFFFFFFFFFFFFFF","E1E1E1E1F0F0F0F0","1E1E1E1E0F0F0F0F"]
key1 = random.choice(keys).decode("hex")
des1 = DES.new(key1, DES.MODE_ECB)
plaintext="CCSC{74k3_0ff_y0ur_p4n75_4nd_y0ur_p4n7135,_5h17_0n_7h3_fl00r!!!}"
ciphertext1 = des1.encrypt(plaintext)
ciphertext1 = base64.b64encode(ciphertext1)
print ciphertext1