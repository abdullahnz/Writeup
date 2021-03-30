#!/usr/bin/python

from itertools import product
from pwn import p64

charset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

def logic(n):
    res = ''
    for x in range(4):
        tmp = n >> (6 * x)
        idx = tmp & 0x3f
        res += charset[idx]
    return res

mapping = {}

for c in product(charset, repeat=3):
    c = ''.join(c)
    d = c.encode('hex')
    d = int(d, 16)
    mapping[logic(d)] = c

