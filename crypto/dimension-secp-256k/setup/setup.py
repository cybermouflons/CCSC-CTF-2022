import random
import time
import json

from hexbytes import HexBytes
from web3 import Web3
from base64 import b64encode

from eth_account._utils.legacy_transactions import (
    serializable_unsigned_transaction_from_dict,
    encode_transaction
)

from pycoin.ecdsa.secp256k1 import secp256k1_generator
from pycoin.ecdsa.intstream import from_bytes

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

PROVIDER_URL = "https://rinkeby.infura.io/v3/9f596b1e11184492aee2980d29fca575"
PRIVATE_KEY = "d7106d464b6626ce222affa14193a10a883de948bf36c254be924eb2c3e0bed7"
WALLET_ADDRESS = "0x42d553C08E1Dcc1180c214fE36753Eb2Ebd4F576"
TO_ADDRESS = "0x0000000000000000000000000000000000000000"
CHAIN_ID = 4
ECDSA_K = 1337
FLAG = open("flag.txt", "rb").read()

def encrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ciphertext).decode('utf-8')
    return json.dumps({'iv':iv, 'ciphertext':ct})

messages = [
    b"Good job!",
    b"Keep looking",
    b"You are on the right path!",
    FLAG,
    b"Wubba Lubba Dub Dub!",
    b"Sometimes science is more art than science."
]

random.shuffle(messages)

print(messages)

aes_key = bytes.fromhex(PRIVATE_KEY)
tx_data = [encrypt_data(message, aes_key) for message in messages]

web3 = Web3(Web3.HTTPProvider(PROVIDER_URL))

idx = 0
errs = 0
while True:
    data = tx_data[idx]
    print("========== TX_NO: {0} =========".format(idx))
    nonce = web3.eth.getTransactionCount(WALLET_ADDRESS)
    gasPrice = web3.toWei('5', 'gwei')
    value = web3.toWei(0.0, 'ether')

    tx = {
        'nonce': nonce,
        'to': TO_ADDRESS,
        'value': value,
        'gas': 210000,
        'gasPrice': gasPrice,
        'data': data.encode("utf-8"),
    }

    try:
        if idx in [0, len(tx_data) - 1]: # reuse nonce for first and last transaction
            k = ECDSA_K
        else:
            k = random.randint(1,99999999)

        print("Sending tx with static nonce {0}....".format(k))
        # Send transaction with modified nonce
        unsigned_transaction = serializable_unsigned_transaction_from_dict(tx)
        transaction_hash = from_bytes(unsigned_transaction.hash(), "big")

        # chain_id = 4
        # v = 0 + chain_id * 2 + 35
        (r,s) = secp256k1_generator.sign(from_bytes(bytes.fromhex(PRIVATE_KEY), "big"), transaction_hash, lambda *args: k)
        encoded_transaction = HexBytes(encode_transaction(unsigned_transaction, vrs=(27, r, s))) # v depends on internal coordinates while signature generation so that public key is recoverable. For convenience i just have it static here and retrying if something wents wrong..
        print(encoded_transaction.hex())

        tx_hash = web3.eth.send_raw_transaction(encoded_transaction)

        print(web3.toHex(tx_hash))
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print(receipt)
        
        # print("Sending tx normally....")
        # # ## Send a transaction normally
        # signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        # tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        # print(web3.toHex(tx_hash))
        # receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        # print(receipt)
        errs = 0
        time.sleep(2)
        if idx == len(tx_data) -1:
            break
        idx += 1
    except ValueError as e:
        print(e)
        errs += 1
        if errs > 20:
            idx -= 1
            errs = 0

template = """Note: All transactions happened on Rinkeby Ethereum network. Other networks are irrelevant to the challenge.

{1}"""
with open("../public/address.txt", "w") as f:
    f.write(template.format(WALLET_ADDRESS))