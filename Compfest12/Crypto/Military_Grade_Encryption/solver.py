#!/usr/bin/python

def xorrr(a, b):
    return [chr(ord(i)^ord(j)) for i,j in zip(a, b)]

not_flag_enc = open('not_flag.enc').read()
not_flag_txt = open('not_flag.txt').read()

key = xorrr(not_flag_enc, not_flag_txt)
flag = open('flag.enc').read()

print "".join(xorrr(flag, key))
