#!/usr/bin/python3

from binascii import *
import random

p = 101
q = 211 
n = 21311 # hint: n = p*q

encrypted_flag = [ ord(d) for d in open('enc', 'r').read() ]

random.seed(q)
stage_one = []
for i in range(10, len(encrypted_flag)+10):
    i -= 1
    z = p + q - i
    stage_one.append(encrypted_flag[i - 9] ^ random.randint(i, z))

flag = ''
for a in stage_one:
    b = a % 5
    flag += chr((a-b)//5)

print(flag[:-1])
