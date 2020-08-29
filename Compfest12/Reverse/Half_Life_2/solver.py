#!/usr/bin/python


def base36encode(s):
    charset = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    result = ''
    while(s):
        a = s/36
        b = 36*a
        result += charset[s-b]
        s = a
    return result[::-1]

cipher = 16166842727364078278681384436557013
    
b = base36encode(cipher)
print ''.join([chr((ord(i)-97-24)%26+97) for i in b])
