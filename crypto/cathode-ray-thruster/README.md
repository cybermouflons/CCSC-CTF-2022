# Cathode Ray Thruster 
**Category:** crypto

**Author:** _Rok0'sBasilisk_

## Description

Hey, Morty! Are you ready for an adventure? \*burp\*. We gotta jump into the microverse and teach that arrogant Zeep a lesson! This Cathode Ray Thruster is gonna make all their motherboards go faulty ... \*burp\*

## Solution
<details>
 <summary>Reveal Spoiler</summary>

This is a classic fault injection attack on RSA-CRT signature.

Participants must exploit a race condition by sining a message and at the same time hitting the motherboard with lasers (3rd option in the menu). If timed right, it will result to a different (faulty) signature for the same message which can be used to recover the private key and therefore decrypt the flag.

See [solve.py](solution/solve.py) for a working exploit.

EDIT: Or... just send the encrypted flag to be signed, and the script will gladly return the decryption for you since I was lazy enough to not hash the message to be signed xD xD. Thanks to @canopus for pointing this unintended solution. And kudos to everyone that solved the challenge in either way. 

</details>
