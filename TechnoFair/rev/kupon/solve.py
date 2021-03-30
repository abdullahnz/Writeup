#!/usr/bin/python

from itertools import product

binary = open('chall').read()
charset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

def logic(n):
    res = ''
    for x in range(4):
        tmp = n >> (6 * x)
        idx = tmp & 0x3f
        res += charset[idx]
    return res

def parseKey(s):
    r = []
    for i in range(0, len(s), 5):
        r += [s[i+1:i+5]]
    return ''.join(r[::-1])

mapping = {}

for c in product(charset, repeat=3):
    c = ''.join(c)
    d = c.encode('hex')
    d = int(d, 16)
    mapping[logic(d)] = c

# kupon_21579
# kupon_67273
# kupon_31878

flag = ''

some_charset = 'h89+/h4567h0123hwxyzhstuvhopqrhklmnhghijhcdefhYZabhUVWXhQRSThMNOPhIJKLhEFGHhABCD'
binary = binary.split(some_charset)

for i in range(1, len(binary)):
    try:
        c = binary[i][3:38]
        d = binary[i][38+5:64+4]
        
        c = parseKey(c)
        d = parseKey(d) + binary[i][38+4:38+5]

        a = ''
        for i in range(0, len(c), 4):
            try:
                a += mapping[c[i:i+4]][::-1]
            except:
                a += 'bDr' # v0cher ?

        b = ''
        for i in range(len(a)):
            b += chr(ord(a[i]) ^ ord(d[i]))

        if all([cond not in b for cond in 'Maaf Kode Tidak Valid'.split()]):
            print b
            flag += b
    except:
        pass

print flag

# s3l4m4t_1n1_Ad4lah_k0d3_v0cherd1sc0unt_fl4gnya_9945723376055852 (?)
