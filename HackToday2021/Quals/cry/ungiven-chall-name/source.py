import random
from Crypto.Cipher import AES
from hashlib import md5
from base64 import b64decode
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.number import *

# Padding for the input string --not
# related to encryption itself.
BLOCK_SIZE = 16  # Bytes
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


class AESCipher:
    def __init__(self, key):
        self.key = md5(key).hexdigest()
    def encrypt(self, raw):
        raw = pad(raw)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return (cipher.encrypt(raw))
    def decrypt(self, enc):
        cipher = AES.new(self.key, AES.MODE_ECB)
        return unpad(cipher.decrypt(enc))


p = getPrime(1024)
a = getPrime(13)
b = getPrime(13)
g = random.randrange(2,4)
A = pow(a,g,p)
B = pow(b,g,p)
s = pow(B,a,p)

print("""
A : {0}
B : {1}
P : {2}
""".format(A,B,p))

aes = AESCipher(str(s))
flag = open("flag.txt","rb").read()
print(aes.encrypt(flag).encode("hex"))

