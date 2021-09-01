#!/usr/bin/env python3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.number import getRandomNBitInteger

# FLAG = open('flag.png', 'rb').read()

class Bread:
    def __init__(self, state, switch=True):
        assert state.bit_length() <= 64
        self.state = state
        self.switch = switch
        self.mask32 = (1 << 32) - 1
        self.mask64 = (1 << 64) - 1

    def encrypt(self, message):
        key = b''.join([int.to_bytes(self.next(), 4, 'big') for _ in range(4)])
        iv  = b''.join([int.to_bytes(self.next(), 4, 'big') for _ in range(4)])
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(pad(message, 16))

    def next(self):
        # print(self.state)
        self.state = ((self.state << 43) | (self.state >> (64 - 43))) & self.mask64
        # print(self.state)
        self.state = self.state ^ int.from_bytes('🍞'.encode(), 'big')
        # print(self.state)
        self.switch = not self.switch
        return (self.state >> 32) & self.mask32 if self.switch else self.state & self.mask32

def main():
    seed = getRandomNBitInteger(64)
    # print(bin(seed)[2:])
    bread = Bread(seed)
    bread.next()
    bread.next()

    # enc = bread.encrypt(FLAG)
    # with open('flag.enc', 'wb') as f:
    #     f.write(enc)
    #     f.close()

if __name__ == '__main__':
    main()
