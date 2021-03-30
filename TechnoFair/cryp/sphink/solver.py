#!/usr/bin/python

from pwn import *
from randcrack import RandCrack

HOST = '103.152.242.172'
PORT = 7070

def getSphinx(n):
    r.sendlineafter('[>] ', str(n))
    r.recvlines(2)
    out = r.recvline(0)
    if 'sphinx!' in out:
        return 'found'
    return int(out.split()[-1])


r = remote(HOST, PORT)

rc = RandCrack()

for n in range(1, 1338):
    rand = getSphinx(n)
    if rand == 'found':
        break
    if n < 625:
        rc.submit(rand)
    else:
        predict = rc.predict_getrandbits(32)
    
predict = rc.predict_getrandbits(32)
print 'PREDICT: ' + str(predict)
r.sendlineafter('[>]', str(predict))
# technofair{1s_this_even_crypt0graphy?}

r.interactive()

