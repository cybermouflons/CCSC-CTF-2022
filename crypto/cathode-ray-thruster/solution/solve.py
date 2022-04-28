from concurrent.futures import ThreadPoolExecutor
from Crypto.Util.number import bytes_to_long, GCD, long_to_bytes

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
modulus = 831922341027016495921650623257797618095060924065814866469076287911348909798276040559320015401463727532280728955265439930701145555331570711114416530106758072413352911909115651549429846545741506755634190538453362960396606981583760544885102807648801243571558080130625302631955941856042999596519287215433778310026592542050317733519994311009633282600065471638253568011510648657629395847106168838380814906284558171109927094482752642607523071876251592721574137623941942293234692266366597708101743843168297255030434199770165311556035741131015344965834405750296442760037007279819992239685083915863783761861124650704579400080839489314108603861743694810190871971382774395199205979096550571621707391690995009084713041149222906819353910643313919128232886886178938742487848665682322423601326812209436424851873966729304387924509833612277546683392203403154274215662964366794575973200166955699632320830446820914524531144882165040400397816960548246454135519004097219628330094404092791134857823185815929801336706771630969151973492174821564868508032613879665478753895829687373266377217994797494062666318160705492397139120991861103914660038310872480381382678024011107134525009418431158594022386457517793167270644378157742512493730285467039983860671725659
public_exponent = 65537
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