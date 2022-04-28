import sympy
import math
from Crypto.Cipher import AES
### https://en.wikipedia.org/wiki/Convergent_series

x, k = sympy.symbols('x k', integer=True)

def KDF(KDFs,X):
	global x, k
	key = []
	for i in range(len(KDFs)):
		result = KDFs[i].subs(x, X[i]).evalf()
		key.append(f"{result:.7f}")
	return "".join(key).replace(".","")
	
#alternating harmonic series = ln2
f1 = sympy.Sum(1/(2*k-1), (k, 1, x)) - sympy.Sum(1/(2*k), (k, 1, x))
#reciprocals of factorials = exp
f2 = sympy.Sum(1/sympy.factorial(k), (k, 0, x)) 
#reciprocals of square numbers = (pi^2)/6
f3 = sympy.Sum(k**-2, (k, 1, x))
#fibonacci series = psi
f4 = sympy.Sum(1/sympy.fibonacci(k), (k, 1, x))
#negative infinity = exp(2/3)/5
f5 = sympy.sympify("(exp(x)+exp(2/3))/5",locals={'x': x})
#negative infinity = exp(23/11)/97
f6 = sympy.sympify("(exp(23/11)+exp(-x))/97",locals={'x': x})

key_funcs = [f1,f2,f3,f4]
key_X = [10000000000,100,100000000,100]
key = KDF(key_funcs,key_X)

IV_funcs = [f5,f6]
IV_X = [-100,100]
IV = KDF(IV_funcs,IV_X)

print("key",key)
print("IV",IV)


####Encrypt
#plaintext = b"CCSC{C0nv3rging_K3y_G3n3r4t1on_Functions_4r3_ind33d_G00fy!1!1!1}"
#cipher = AES.new(bytes(key,"utf-8"), AES.MODE_CBC,iv=bytes(IV,"utf-8")) 
#ciphertext = cipher.encrypt(plaintext)
#print(ciphertext)


flag = b"#\x98\x8by\xb7\xe0\xd6\x90\xdb\xbd \xaen\x9c\xc4\nE\x88\xd1#M\x84A\xd2\xb1\xc5\xeb\x0e^\x1a\x84J\x14\xb5\xfbJ\x0e\xcb\x85\x00g\xf9\xe7k\x05\x8d\x9aU\xf8\xa1\x84F\xadT\xfb\xde\xd4\x85\xe4\xbe\xf13Op"

cipher = AES.new(bytes(key,"utf-8"), AES.MODE_CBC,iv=bytes(IV,"utf-8")) 
plaintext = cipher.decrypt(flag)
print(plaintext)




######## AES CBC
## key = 06931472271828181644934133598857    
## IV = 0389546800834254
## plaintext = b"CCSC{C0nv3rging_K3y_G3n3r4t1on_Functions_4r3_ind33d_G00fy!1!1!1}"
## ciphertext = b"#\x98\x8by\xb7\xe0\xd6\x90\xdb\xbd \xaen\x9c\xc4\nE\x88\xd1#M\x84A\xd2\xb1\xc5\xeb\x0e^\x1a\x84J\x14\xb5\xfbJ\x0e\xcb\x85\x00g\xf9\xe7k\x05\x8d\x9aU\xf8\xa1\x84F\xadT\xfb\xde\xd4\x85\xe4\xbe\xf13Op"
###########