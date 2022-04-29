import random
import socketserver
import time

from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes

HOST = "0.0.0.0"
PORT = 9000
FLAG = open("flag.txt", "r").read().strip()
RSA_PARAMS = RSA.importKey(open("./private-key.pem", "r").read().strip())

assert RSA_PARAMS.p > RSA_PARAMS.q

dp = 0

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b%a,a)
    return (g, x - (b//a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    return x%m

def s2n(s):
    return bytes_to_long(s if type(s) is bytes else bytearray(s, "latin-1"))

def n2s(n):
    return long_to_bytes(n).decode("latin-1")

def recvline(req) -> bytes:
    buf = b""
    while not buf.endswith(b"\n"):
        buf += req.recv(1)
    return buf

def intro_banner() -> bytes:
    return bytes(
        "\n====================================\n"
        "          Miniverse Battery \n"
        "====================================\n"
        "1. print encrypted flag\n"
        "2. sign message\n"
        "3. hit with laser\n"
        "====================================\n",
        'utf-8'
    )

def encrypt_flag():
    return pow(s2n(FLAG), RSA_PARAMS.e, RSA_PARAMS.n)


def sign_message_prompt(req):
    req.sendall(b"Please type a message to sign: ")
    message = s2n(recvline(req).strip())

    if message >= RSA_PARAMS.n:
        return b"Message has to be smaller than public modulus"

    return sign_message(message)


def sign_message(m: int):
    global dp

    dp = RSA_PARAMS.d % (RSA_PARAMS.p - 1)
    dq = RSA_PARAMS.d % (RSA_PARAMS.q - 1)

    time.sleep(0.1)

    s1 = pow(m, dp, RSA_PARAMS.p)
    s2 = pow(m, dq, RSA_PARAMS.q)

    qInv = modinv(RSA_PARAMS.q, RSA_PARAMS.p)

    h = (qInv * (s1-s2)) % RSA_PARAMS.p
    return s2+h*RSA_PARAMS.q

def laser_hit():
    global dp
    dp_bytes = n2s(dp)
    dp ^= 1 << (8*random.randint(0,len(dp_bytes)-1) + random.randint(0,7))
    return b"** Strange laser noises **"

def to_hex(func, *args, **kwargs):
    def wrapper():
        res = func(*args, **kwargs)
        return (b'0x%0512x\n' % res) if type(res) == int else res
    return wrapper

def challenge(req):
    menu = {
        "1": to_hex(encrypt_flag),
        "2": to_hex(sign_message_prompt, req),
        "3": laser_hit,
    }

    req.sendall(intro_banner())
    req.sendall(b"Please choose an option: ")

    choice = req.recv(2).strip().decode("latin-1")

    if choice not in menu:
        exit(1)

    req.sendall(menu[choice]())

class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            challenge(self.request)


class ChallengeTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    ...


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    server = ChallengeTCPServer((HOST, PORT), Handler)
    print("Starting server {0}:{1}".format(HOST, PORT))
    server.serve_forever()
