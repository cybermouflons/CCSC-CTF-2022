flag = b"#\x98\x8by\xb7\xe0\xd6\x90\xdb\xbd \xaen\x9c\xc4\nE\x88\xd1#M\x84A\xd2\xb1\xc5\xeb\x0e^\x1a\x84J\x14\xb5\xfbJ\x0e\xcb\x85\x00g\xf9\xe7k\x05\x8d\x9aU\xf8\xa1\x84F\xadT\xfb\xde\xd4\x85\xe4\xbe\xf13Op"

def KDF(KDFs,X):
	key = []
	for i in range(len(KDFs)):
		result = KDFs[i](X[i])
		key.append(f"{result:.7f}")
	return "".join(key).replace(".","")

key = KDF()
IV = KDF()

def decrypt(flag, key, IV):
	cipher = AES.new(bytes(key,"utf-8"), AES.MODE_CBC, iv=bytes(IV,"utf-8")) 
	plaintext = cipher.decrypt(flag)
	return plaintext
