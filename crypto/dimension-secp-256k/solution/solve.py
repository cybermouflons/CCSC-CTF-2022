import sha3
import json
from base64 import b64decode

from Crypto.Cipher import AES
from ecdsa import SECP256k1, ecdsa
from ecdsa.numbertheory import inverse_mod
from ecdsa.keys import SigningKey

import rlp
from eth_account._utils.legacy_transactions import (
    serializable_unsigned_transaction_from_dict,
)
from pycoin.ecdsa.intstream import from_bytes
from eth_keys.backends.native.ecdsa import ecdsa_raw_recover, decode_public_key
from web3 import Web3

PROVIDER_URL = "https://eth-rinkeby.alchemyapi.io/v2/aKg4Pu606zQdaWJLPFurzzFjPsUvDSiZ"

web3 = Web3(Web3.HTTPProvider(PROVIDER_URL))

txids = [
    "0x89fcbe1b8c8e6f18c0fe34a59ec949630c4b5dd0603a5d2e729ed9cb0ac658d4",
    "0x9cf1fd0e8b53094cfb18fa9d7b995e0a767a0daa26d050c1e2329d84e35cf293",
    "0x07301dd5af1f151470570cfacb74380196925a4bf9aeb90bdc5e719f15d30437",
    "0xe2cb0bae1192e1ae9a2dad0b6613509ac1ce04c60eaa5816ef4c2d10a7674ee0",
    "0x7509c7c408957a944ff4d8b34f0df4a93be91a595dc360b26ad003dc9291fb49",
    "0x420ced3b2cbdb2ee87d97edb738113667fbc6ccde1d96fb26e754e47b0100d12"
]


def get_transaction_info(txid):
    tx_dict = web3.eth.get_transaction(txid)
    tx_unserialized = {
        'nonce': tx_dict["nonce"],
        'to': tx_dict["to"],
        'value': tx_dict["value"],
        'gas': tx_dict["gas"],
        'gasPrice': tx_dict["gasPrice"],
        'data': bytes.fromhex(tx_dict["input"][2:]),
    }
    unsigned_tx = serializable_unsigned_transaction_from_dict(tx_unserialized)

    return {
        "raw_tx": rlp.encode(unsigned_tx),
        "hash": unsigned_tx.hash(),
        "tx_dict": tx_dict,
    }
txs_data =[get_transaction_info(txid) for txid in txids]

def find_nonce_reuse(txs_data):
    for tx_1 in txs_data:
        for tx_2 in txs_data:
            if tx_1["tx_dict"]["hash"] == tx_2["tx_dict"]["hash"]:
                continue
            
            if tx_1["tx_dict"]["r"] == tx_2["tx_dict"]["r"]:
                print("Found nonce reuse!")
                return [tx_1, tx_2]
    return []

nonce_reuse_txs = find_nonce_reuse(txs_data)

tx_hsh = txs_data[0]["hash"]
tx_vrs = (txs_data[0]["tx_dict"]["v"]-27, from_bytes(txs_data[0]["tx_dict"]["r"], "big"), from_bytes(txs_data[0]["tx_dict"]["s"], "big"))
pub_key_point = decode_public_key(ecdsa_raw_recover(tx_hsh, tx_vrs))
signature = ecdsa.Signature(r=tx_vrs[0], s=tx_vrs[1])

verbosity = 2
def recover_from_hash(curve, r, s1, h1, s2, h2, hashfunc):
    """
    :param curve:
    :param r:
    :param s1:
    :param h1:
    :param s2:
    :param h2:
    :param hashfunc:
    :return:
    """
    # Extract order from curve
    order = curve.order

    # Precomputed values for minor optimisation
    r_inv = inverse_mod(r, order)
    h = (h1 - h2) % order

    #
    # Signature is still valid whether s or -s mod curve_order (or n)
    # s*k-h
    # Try different possible values for "random" k until hit
    for k_try in (s1 - s2,
                  s1 + s2,
                  -s1 - s2,
                  -s1 + s2):

        # Retrieving actual k
        k = (h * inverse_mod(k_try, order)) % order

        if verbosity >= 2:
            print("Trying nonce value : '{}'".format(k))

        # Secret exponent
        secexp = (((((s1 * k) % order) - h1) % order) * r_inv) % order

        if verbosity >= 2:
            print("Secret exposant : '{}'".format(secexp))

        # Building the secret key
        signing_key = SigningKey.from_secret_exponent(secexp, curve=curve, hashfunc=hashfunc)

        # Verify if build key is appropriate
        if signing_key.get_verifying_key().pubkey.verifies(h1, ecdsa.Signature(r, s1)):
            if verbosity >= 1:
                print("Success !")
            return signing_key

    return None

r = from_bytes(nonce_reuse_txs[0]["tx_dict"]["r"], "big")
s1 = from_bytes(nonce_reuse_txs[0]["tx_dict"]["s"], "big")
h1 = from_bytes(nonce_reuse_txs[0]["hash"], "big")
s2 = from_bytes(nonce_reuse_txs[1]["tx_dict"]["s"], "big")
h2 = from_bytes(nonce_reuse_txs[1]["hash"], "big")

## ATTACK
private_key = recover_from_hash(SECP256k1, r, s1, h1, s2, h2, hashfunc=sha3.keccak_256).privkey

## DECRYPT FLAG
for tx_data in txs_data:
    tx_input_decoded = json.loads(bytes.fromhex(tx_data["tx_dict"]["input"][2:]).decode("ascii"))
    iv = b64decode(tx_input_decoded["iv"])
    enc_data = b64decode(tx_input_decoded["ciphertext"])
    cipher = AES.new(private_key.secret_multiplier.to_bytes(32, byteorder='big'), AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(enc_data)
    if plaintext.startswith(b"CCSC{"):
        print("FLAG: ", plaintext)
        break
