#!/usr/bin/python3

from binascii import unhexlify
from itertools import product

class QCX:
    def __init__(self, array):
        S = [0] * 256
        T = [0] * 256
        keylen = len(array)
        for i in range(256):
            S[i] = i
            T[i] = array[i % keylen]
        n = 0
        for i in range(256):
            n = ((n + S[i] + T[i]) & 0xFF)
            S[n], S[i] = S[i], S[n]

        self.S = S
        self.T = T

    def validate(self):
        hexstr = unhexlify(b'91AD6CC96F93D0B1C41426A98E5E5C8BA6A372045EC20D21D2097257229C69779C69F699E09E6A74A45B587E085516E7CDE8')
        result = [0] * len(hexstr)
        x = 0
        y = 0
        for i in range(len(hexstr)):
            x = ((x + 1) & 0xFF)
            y = ((y + self.S[x]) & 0xFF)
            self.S[y], self.S[x] = self.S[x], self.S[y]
            result[i] = bytes([hexstr[i] ^ self.S[(self.S[x] + self.S[y]) & 0xFF]])
        return b''.join(result)


def XQC_hash(array):
    n = -3750763034362895579
    n2 = 1099511628211
    for i in range(len(array)):
        n = (n ^ (array[i] & 0xFF)) * n2

    result = [0] * 8
    for i in range(7, -1, -1):
        result[i] = (n & 0xFF)
        n >>= 8
    return result

if __name__ == "__main__":
    '''
    ```
    symbols = ["Pepega", "xqcL", "Book", "EZ", "Clap", "OMEGALUL", "FeelsGoodMan", "TriHard"]
    for key in product(symbols, repeat=7):
        key = XQC_hash(''.join(key).encode())
        dec = QCX(key).validate()
        if b'hacktoday' in dec:
            print(prod)
            print(dec)
            break
    ```
    
    ❯  time python3 solve.py
    ('EZ', 'Clap', 'Book', 'Book', 'Book', 'xqcL', 'FeelsGoodMan')
    b'hacktoday{dream_luck_or_cheating_it_is_what_it_is}'

    real	2m43,267s
    user	2m43,013s
    sys	0m0,157s
    '''

    key = ['EZ', 'Clap', 'Book', 'Book', 'Book', 'xqcL', 'FeelsGoodMan']
    key = ''.join(key)
    key = XQC_hash(key.encode())

    print(key)
    print(QCX(key).validate())

    