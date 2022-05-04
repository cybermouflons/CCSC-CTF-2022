import random
import json

HOST = "0.0.0.0"
PORT = 13373

lottery_id = 0

f = open("flag.txt", "r")
flag = f.read()
f.close()

print("Play lottery and win a flag!", flush=True)
while True:
    guess = input()
    winner = random.getrandbits(32)
    won = "%d" % winner == guess.strip()
    resp = {
        "won": won,
        "flag": (won and flag) or None,
        "lottery_id": lottery_id,
        "winner": winner,
    }
    lottery_id += 1
    if not guess:
        break
    print(json.dumps(resp), flush=True)
