# Dimension SECP-256K1
**Category:** crypto, blockchain

**Author:** _Rok0'sBasilisk_

## Description

Do you see this, Morty? It all looks normal in this dimension but watch out! Weird things can happen if you are not careful... 

## Solution
<details>
 <summary>Reveal Spoiler</summary>

 This challenges presents an Ethereum address to the participants.

 Inpecting the activity of the address in the Rinkeby network as instructed in the challenge files, one can observer that this address has performed 6 transactions to the 0 address. Since the recipient is the zero address and given that this is a crypto challenge participants should not focus on the trail of funds but rather on the transactions themselves. 

 A hint is provided in the challenge title which highlights the curve that is used in Ethereum blockchain for digital signatures.

 By fetching the transactions and inspecting their signatures participants should notice that all of them contain some data in the input and there are two of them with the same "r" value. That's a classic for nonce-reuse attack.

 With a nonce-reuse attack, the private key of the address is recoverable.

 By converting the transactions' input data to ascii, a json structure is revealed of the format {"iv":.. ,"ciphertext": ...} which hints to AES-CBC cipher (because of the iv). 

 Participants must then make the connection and use the recoverable private key as AES key and decrypt the data. One of the transaction contains the flag in its data.

 For a solution coded in python checkout [solve.py](solution/solve.py).

</details>