import random as ciwi
from binascii import *

p = 101
q = 211 
n = 21311 # hint: n = p*q

flag = "COMPFEST{testing}" # redacted

enc = ""
for i in flag:
    enc += chr((5 * ord(i)) + ciwi.randint(1,4))

ciwi.seed(q)

print(enc)

enc2 = ""
for i in range(10, len(enc) + 10):
    i -= 1
    z = p + q - i
    enc2 += chr(ord(enc[i - 9]) ^ ciwi.randint(i, z))

print(enc2)
