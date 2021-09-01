#!/usr/bin/python3

from base64 import *

choose = list(b'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789qwer')
output = list(b'PIQ7ZrYSqROWT3J1HFUX05498DwVGC2EBNAL6eMK')

shuffled_index = []

for c in choose:
    shuffled_index += [output.index(c)]

print(f'Shuffled index = {shuffled_index}')

shuffled = open('flag.txt', 'rb').read()
flag = b''

for index in shuffled_index:
    flag += bytes([shuffled[index]])

print(f'Encoded flag = {flag}')
print(f'Flag = {b64decode(flag)}')
