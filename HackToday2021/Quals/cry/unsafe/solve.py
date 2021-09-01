#!/usr/bin/python3

from itertools import product
from binascii import unhexlify
from time import time

flag = [50, 51, 55, 48, 50, 974, 49, 970, 50, 53, 50, 968, 55, 48, 50, 969, 49, 970, 49, 970, 49, 970, 50, 973, 50, 51, 50, 969, 49, 970, 50, 54, 50, 53, 50, 974, 51, 49, 49, 970, 50, 60, 50, 53, 50, 969, 51, 48, 55, 48, 50, 968]

key = 10000

x = key - 1000 - 1
y = key + 1000

xor = lambda x, y: int(f'{x ^ (y ** 2)}'[5:])

charset = [ord(c) for c in '0123456789abcdef']

start = time()

while x < y:
    x += 1
    for p in product(charset, repeat=3):
        a = xor(p[0], x)
        b = xor(p[1], x)
        c = xor(p[2], x)
        if [a, b, c] == flag[:3]:
            p = chr(p[0]) + chr(p[1]) + chr(p[2])
            f = b''
            for i in range(len(flag)):
                for k in charset:
                    if xor(k, x) == flag[i]:
                        f += bytes([k])
                        break
            if len(f) % 2 == 0:
                sec = int(time() - start)
                print(f'Posible key: {x} (time {sec}s)')
                print(f'Flag: {unhexlify(f)}')
                