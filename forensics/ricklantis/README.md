# FakeDoor

**Category**: forensics

**Author**: anderson101

## Description

TBD

<details>
<summary>Reveal Spoiler</summary>

Flag: `CCSC{Z1ger1ons_rock_you_morty2837}`

AS-REP Roast Attack
1. The challenge is an analysis of a packet capture of a AS-REP attack.
2. First filter the packets using "kerberos" keyword
3. Packet #40 AR-REP (dst.ip 10.66.6.6 length 1450) holds the encrypted timestamp
4. Extract the data from enc-part:cipher
5. Reconstuct the hash for cracking with hashcat

$krb5asrep$23$morty@RICKLANTIS.LOCAL:f05bb662775764d1bfbae3e0da153e3b$6619299b83b46a768c51cc32c9b7153fc00863505d35ab0c435e69cf06af4a86f9beadf472dfb691f7ca51196ac208fa2b318b943602ca25232f5d1e3b002ef24da84b118f2a2dcf32b7749355484f4a20265927f857694749842f1631a963e9a2a35681f55a939f37914563e083e32e8c322a5ecb7e022d79c54055443988f46698c817097d3d87f840ad85dd1b6df3f5f56a050ba077fd51d627802a7e0c1b9ccb65d8de29dabe4a6d9b4ac8435918f4c0fda0e8d1c2e2040354841776eb73e8b502cd4f5ac695d342477db81cc229ce5d310bee4bbd8cd452613163b22ca60d459fc9416e048cc48e8aeaef158b4bb7feb4b3

6. Use the constucted hash and crack it to find the password. Use the rockyou dictionary.
7. To build the flag, extract png image from the SMB traffic. File --> Export Objects --> SMB...
8. Save the file "where is my coffee morty.png"
9. The png contains part of the flag "CCSC{Z1ger1ons_rock_you_CRACKEDPASS}" and needs to be combined with the cracked password.

Hints:
a. The png that holds the flag contains hints to construct the krb5 hash
b. Another png, "what is this rick.png" contans the correct structure of the hash. 
   The string that is displayed, when they search for it, direct them to the following article:
   https://blog.xpnsec.com/kerberos-attacks-part-2/

</details>
