#!/usr/bin/python3
from random import randint

def gen_pk(n):
    return randint(n-1000,n+1000)

def encrypt(msg,pk):
    cip = ""
    for i in msg:
        cip += str(ord(i) ^ pk**2)+" "
    return cip.split()

flag = open("flag").read().strip().encode().hex()
pk = gen_pk(10000)
enc = []
c_flag = encrypt(flag,pk)

for i in c_flag:
    enc += [int(i[5:])]

print(pk)
#???
print(enc)
#[50, 51, 55, 48, 50, 974, 49, 970, 50, 53, 50, 968, 55, 48, 50, 969, 49, 970, 49, 970, 49, 970, 50, 973, 50, 51, 50, 969, 49, 970, 50, 54, 50, 53, 50, 974, 51, 49, 49, 970, 50, 60, 50, 53, 50, 969, 51, 48, 55, 48, 50, 968]