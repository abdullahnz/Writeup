from Crypto.Cipher import AES
from pwn import *
from binascii import unhexlify
import itertools, os

r = remote('128.199.104.41', 25300)

def choice(num):
    r.sendlineafter('Please select a lab member (or 0 to break): ', str(num))
    r.recvuntil('0.')
    return r.recvline()

def decrypt(cipher):
    enc = hex(int(cipher))[2:].rstrip('L')
    aes = AES.new('supersecretvalue', AES.MODE_ECB)
    dec = aes.decrypt(enc.decode('hex'))
    return dec

for i in range(1, 12):
    try:
	info(decrypt(choice(i)))
    except:
        pass

