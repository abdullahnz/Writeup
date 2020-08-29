from subprocess import PIPE, Popen
import subprocess
import sys

def cmd(command):
    proc = subprocess.Popen(str(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return proc.communicate()

batman = cmd('md5sum 0.png')[0].split()[0]
nightwing = cmd('md5sum 1.png')[0].split()[0]
biner = "0"

for i in range(359):
    out = cmd('md5sum {}.png'.format(i))[0].split()[0]

    if out == batman:
        biner += "1"
    else:
        biner += "0"

flag = ''
for i in range(0, len(biner), 8):
    flag += chr(int(biner[i:i+8], 2))

print flag