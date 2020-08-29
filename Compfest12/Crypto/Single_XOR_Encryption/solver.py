#!/usr/bin/python

cipher = open('soal').read().decode('hex')

for i in range(256):
    flag = ""
    for c in cipher:
        flag += chr(ord(c) ^ i)
    if 'COMPFEST' in flag:
        print i, flag
        break
