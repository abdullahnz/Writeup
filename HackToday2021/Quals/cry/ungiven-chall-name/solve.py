#!/usr/bin/python3

from Crypto.Cipher import AES
from Crypto.Util.number import *
from hashlib import md5
from binascii import unhexlify
from gmpy2 import iroot

A = 186854936813
B = 147114332639
P = 163104631519618913258443402849202863277971409891487242879846674663587866056771660251348557779064845523329862553842362843878871618333023175937081392339005234218081151366615642746338575919589454375794289798069149050786541312456216290437739210850531941750546580699722660500820188051579113335793905068023664432841

enc = unhexlify('ea5f1666a512ef7a39a61f70bb36ce46005c7635bbb5727d28fabd40d39a9ca5196f81722d4b4a5612d9ca8d0ed8d333')

'''
p = getPrime(1024)
a = getPrime(13)
b = getPrime(13)
g = random.randrange(2,4)
A = pow(a,g,p)
B = pow(b,g,p)
s = pow(B,a,p)

aes = AESCipher(str(s))
'''

for g in range(2, 5):
    a, cond = iroot(A, g)
    if cond:
        break

print(f'Found a: {a}')
print(f'Found g: {g}')

key = f'{pow(B, a, P)}'.encode()
key = md5(key).hexdigest().encode()

print(f'Calc key: {key}')

aes = AES.new(key, AES.MODE_ECB)
print(f'Flag: {aes.decrypt(enc)}')


