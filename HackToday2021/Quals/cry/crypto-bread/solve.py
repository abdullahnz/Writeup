#!/usr/bin/python3

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import getRandomNBitInteger
from chall import Bread

'''
...
01010100010 100000111110111000100 10100101011100010111111100010011
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx10100101011100010111111100010011
10001011111110001001101010100010xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx00110100010010101001111010110000
01010100111101011000000101000110xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
...
1010101110010100001011001011011101100011011111110111101100011000
1111101111011000110001010101110010100001011001011011101100011011

'''

encrypted = open('flag.enc', 'rb').read()

# AES IV
states = encrypted[:16]
states = [int.from_bytes(states[i:i+4], 'big') for i in range(0, len(states), 4)]

print('-'*32)

for s in states:
    print(bin(s)[2:].zfill(32))

print('-'*32)

min = int('1'.ljust(21, '0'), 2)
max = int('1'.ljust(21, '1'), 2)

for missing in range(min, max + 1):
    seed  = (((states[1] & ((1 << 11) - 1)) << 21 | missing) << 32) | states[0]
    bread = Bread(seed, switch=False)
    maybe = [bread.next() for _ in range(3)]
    if maybe == states[1:]:
        print(f'states[5] = {seed}')
        break

rotate = lambda x: int(x[21:] + x[:21], 2)
key = int.from_bytes('🍞'.encode(), 'big')

for i in range(5):
    seed = bin(seed ^ key)[2:].zfill(64)
    seed = rotate(seed)
    print(f'states[{5 - i - 1}] = {seed}')

bread = Bread(seed)

key = b''.join([int.to_bytes(bread.next(), 4, 'big') for _ in range(4)])
iv  = b''.join([int.to_bytes(bread.next(), 4, 'big') for _ in range(4)])

print(f'Found key = {key}')

aes  = AES.new(key, AES.MODE_CBC, iv)
data = aes.decrypt(encrypted[16:])

with open('flag.png', 'wb') as f:
    f.write(data)
    f.close()
