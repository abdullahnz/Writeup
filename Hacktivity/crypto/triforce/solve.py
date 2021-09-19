#!/usr/bin/python3

from pwn import *

HOST = 'challenge.ctf.games'
PORT = 31462

def select_piece(index, start = False):
    if not start:
        r.sendlineafter('# ', '3')
    r.sendlineafter('# ', f'{index}')

def encrypt(pl : bytes):
    r.sendlineafter('# ', '1')
    r.sendlineafter('> ', pl.hex())
    r.recvline(0)
    return r.recvline(0)

def decrypt(ct : bytes):
    r.sendlineafter('# ', '2')
    r.sendlineafter('> ', ct)
    r.recvline(0)
    return r.recvline(0)

def split(s, block_size=32):
    return [s[i:i+block_size] for i in range(0, len(s), block_size)]


r = remote(HOST, PORT)

select_piece(3, start = True)
known = b'A' * 0x30

ct = split(encrypt(known))
zero = b'00' * 0x10
new = ct[0] + zero + ct[0] + ct[1] + ct[2] + ct[3]

dec = split(decrypt(new))

a = bytes.fromhex(dec[0].decode())
b = bytes.fromhex(dec[2].decode())
c = []

for i in range(len(a)):
    c.append(a[i] ^ b[i])

print(bytes(c))

# flag{819f9d8d837
# 21ac4c442b1659f3
# 6df2d}

# https://cedricvanrompay.gitlab.io/cryptopals/challenges/27.html
    
r.interactive()