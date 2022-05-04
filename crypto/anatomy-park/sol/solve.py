import random
import socket
import json


HOST = "127.0.0.1"
PORT = 13373

state = []
idx = 0


def next_state():
    global idx
    if idx == 624:
        for i in range(624):
            y = (
                (state[i] & 0x80000000) + (state[(i + 1) % 624] & 0x7FFFFFFF)
            ) & 0xFFFFFFFF
            next = (y >> 1) & 0xFFFFFFFF
            next ^= (state[(i + 397) % 624]) & 0xFFFFFFFF
            if (y & 1) == 1:
                next ^= (0x9908B0DF) & 0xFFFFFFFF
            state[i] = (next) & 0xFFFFFFFF
        idx = 0
    y = state[idx]
    idx += 1
    y ^= y >> 11
    y ^= (y << 7) & 0x9D2C5680
    y ^= (y << 15) & 0xEFC60000
    y ^= y >> 18
    return y & 0xFFFFFFFF


def unbitshift_right_xor(value, shift):
    i = 0
    result = 0
    while i * shift < 32:
        part_mask = ((0x0FFFFFFFF << (32 - shift)) & 0xFFFFFFFF) >> (shift * i)
        part = value & part_mask
        value ^= part >> shift
        result |= part
        i += 1
    return result


def unbitshift_left_xor(value, shift, mask):
    i = 0
    result = 0
    while i * shift < 32:
        part_mask = ((0x0FFFFFFFF >> (32 - shift)) & 0xFFFFFFFF) << (shift * i)
        part = value & part_mask
        value ^= (part << shift) & mask
        result |= part
        i += 1
    return result


def unapply_transformation(num):
    value = num
    value = unbitshift_right_xor(value, 18)
    value = unbitshift_left_xor(value, 15, 0xEFC60000)
    value = unbitshift_left_xor(value, 7, 0x9D2C5680)
    value = unbitshift_right_xor(value, 11) & 0xFFFFFFFF
    return value


def submit(s, num):
    s.sendall(b"%d\n" % num)
    resp_bytes = s.recv(1024).strip()
    resp = json.loads(resp_bytes)
    return resp


clone_state = []

warmedup = False


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.recv(1024)
    for i in range(624):
        resp = submit(s, 1337)
        while not warmedup and resp.get("lottery_id") % 624 != 0:
            resp = submit(s, 1337)
        warmedup = True
        clone_state.append(unapply_transformation(resp.get("winner")))

    random.setstate((3, tuple(clone_state + [624]), None))

    next_winner = random.getrandbits(32)

    # custom implementation of pythons prng implementation
    # state = [x for x in clone_state]
    # idx = 624
    # next_winner = next_state()

    resp = submit(s, next_winner)
    print(resp.get("flag"))
