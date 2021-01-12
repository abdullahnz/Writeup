# Learning, about ret2libc and leaking memory address from format string bug.

Wkwkwk, ini ditulis lagi karena setelah menang CTF yang diadakan Telkom yaitu **Icyption**. [Writeup](https://abdullahnz.github.io/posts/icyption/final/)

Gak tau, yang pertamanya gak terlalu mentingin CTF, entah kenapa jadi semangat untuk mencoba soal-soal yang lebih sulit lagi. *plus*, setelah writeup hacktoday 2020 ada yang nge-*share*. Tambah semangat lagi belajar PWN.

Mulailah untuk nge-*solve* soal terakhir Asgama 18. *karena cuma punya sisa soal hanya ini, mungkin.*

Terus nge-drive ke soal hacktoday 20. Soalnya bagus (saya gak ikut kompetisi, karena memang belum tertarik), *plus* saya jadi paham tentang ROP, overwrite GOT with format string bug, OOB to leak and write memory & FSOP. (Sumpah, sebelumnya cuma bisa overwrite return address, itupun gak paham. Lol)
Yang terakhir ini *secara umum* belum begitu paham sih, sampai sekarang (saat tulisan ini ditulis) untuk challenge yang menggunakan versi libc > 2.27. Tapi untuk soalnya, *alhamdullillah* paham. Dengan menelusuri flow program saat exit. Nanti dapet, ada intruksi `call qword ptr [rax]` (kalo gak salah) yang rax ini writeable, yaitu terletak dilibc. Dan parameter-nya pun juga bisa dioverwrite dengan string "/bin/sh".

*Note: challenge ini tidak bisa diselesaikan menggunakan one_gadget*

**Lah, kok malah bahas soal hacktoday sih.**
¯\ (ツ) /¯
