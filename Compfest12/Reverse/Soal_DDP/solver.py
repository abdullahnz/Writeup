#!/usr/bin/python2

from string import *

def llx_flag(x, length):
    result = []
    for i in range(length, -1, -1):
        y  = (x>>(8*i))
        z  = (y<<(8*i))
        x -= z
        result.append(int(y))

    return result

target = 120290679218832191630163797978118096998325980286646140214484761791004452553

for length_flag in range(20, 50):
    valid_flag = llx_flag(target, length_flag)

    for i in range(len(valid_flag)):
        temp = valid_flag[i] * 16 % 0xff
        valid_flag[i] = temp - (i+1)

    flag = ''.join([chr(flag) for flag in valid_flag])
    if flag.startswith("COMPFEST"):
        print flag
        break


