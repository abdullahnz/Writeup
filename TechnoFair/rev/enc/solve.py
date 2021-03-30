#!/usr/bin/python

outfile = '6A676A774848663346337547666C75646E68527369754934614961346E634B6916382702460B171A20095B511A0C124632343A391414050637520D6B2C041C57'.decode('hex')

translated_key = outfile[:16] 
keys = outfile[16:32]
ciphertext = outfile[32:]

number = ['9', '2', '8', '1', '3', '5', '0', '7', '6', '4']
upper  = ['E', 'O', 'B', 'V', 'U', 'C', 'J', 'I', 'H', 'P', 'G', 'S', 'X', 'Z', 'K', 'N', 'Y', 'F', 'W', 'M', 'A', 'D', 'R', 'L', 'T', 'Q']
lower  = ['u', 'p', 'l', 'y', 'x', 'q', 'a', 'w', 'j', 'z', 'n', 't', 'r', 'f', 'i', 'b', 's', 'v', 'd', 'o', 'g', 'c', 'h', 'k', 'm', 'e']

test_key = ''
for tk in translated_key:
    if tk.islower():
        test_key += chr(lower.index(tk) + ord('a'))
    elif tk.isupper():
        test_key += chr(upper.index(tk) + ord('A'))
    else:
        test_key += chr(number.index(tk) + ord('0'))

from pwn import xor

# print test_key
# print keys

# randnum = test_key.index(keys[0])

# print randnum

the_key = 'IniKunciRah4siaa'
print xor(ciphertext, the_key)


    










