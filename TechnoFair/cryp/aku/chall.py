from Crypto.Util.number import *
import gmpy2
from secret import flag

p1 = getPrime(512)
p2 = gmpy2.next_prime(p1)
q1 = getPrime(512)
q2 = gmpy2.next_prime(q1)
n = p1*p2*q1*q2
e = 65537
phi = (p1-1)*(p2-1)*(q1-1)*(q2-1)
d = gmpy2.invert(e,phi)
c = pow(bytes_to_long(flag),e,n)

f = open('out.txt', 'w')
f.write('''n: {},
e: {},
c: {}'''.format(n, e,c))
f.close()
