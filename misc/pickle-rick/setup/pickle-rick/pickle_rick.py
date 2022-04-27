import sys
import pickle
import base64

sys.stdout.write("> ")
sys.stdout.flush()

try:
    pickle_rick = base64.b64decode(sys.stdin.readline().strip())

    if len(pickle_rick) > 23:
        print("That's too much of a pickle")
        exit(1)
    
    print(pickle.loads(pickle_rick))
except Exception as e:
    print(type(e), e)
    print("Flip the pickle over.")
    exit(1)

sys.stdin.close()
