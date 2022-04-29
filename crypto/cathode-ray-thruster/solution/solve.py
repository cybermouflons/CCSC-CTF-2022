from concurrent.futures import ThreadPoolExecutor
from Crypto.Util.number import bytes_to_long, GCD, long_to_bytes
from Crypto.PublicKey import RSA

from pwn import *

HOST = "localhost"
PORT = 9000

io = remote(HOST, PORT)

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def get_prompt(io):
    print("Getting prompt...")
    io.recvuntil(b": ")

## STEP 1 Get correct signature
get_prompt(io)
io.sendline(b"2")
get_prompt(io)
io.sendline(b"Test Message")
correct_signature = io.recvline().strip().decode("utf-8")[2:]

## STEP 2 Inject fault and get faulty signature
get_prompt(io)
io.sendline(b"2")

get_prompt(io)

def get_signature():
    io.sendline(b"Test Message")
    return io.recvline().strip().decode("utf-8")[2:]

def laser_hit():
    inject_io = remote(HOST, PORT)
    get_prompt(inject_io)
    inject_io.sendline(b"3")
    return inject_io.recvline().strip()

with ThreadPoolExecutor(max_workers=6) as executor:
    future = executor.submit(get_signature)
    for _ in range(5):
        executor.submit(laser_hit)
    faulty_signature = future.result()

assert faulty_signature != correct_signature

# STEP 3 - Recover private key
rsa = RSA.importKey(open("../public/public-key.pem", "r").read().strip())
modulus = rsa.n
public_exponent = rsa.e
message = bytes_to_long(b"Test Message")

correct_signature = bytes_to_long(bytes.fromhex(correct_signature))
faulty_signature = bytes_to_long(bytes.fromhex(faulty_signature))

verify_correct = pow(correct_signature, public_exponent, modulus)
verify_faulty = pow(faulty_signature, public_exponent, modulus)

p = GCD(modulus, (verify_faulty - message) % modulus)
q = modulus // p

assert(p*q == modulus)

phi = (p-1)*(q-1)
d = modinv(public_exponent, phi)

# STEP 4 - Get Flag
get_prompt(io)
io.sendline(b"1")
flag_enc = io.recvline().strip().decode("utf-8")[2:]
flag_enc = bytes_to_long(bytes.fromhex(flag_enc))
flag = pow(flag_enc, d, modulus)
print("FLAG: ", long_to_bytes(flag))