
cipher = [
    "82ef4cccc87afe8a4cf235c26d2723fcbeb470e10fa7bd7f1ce23d9755772b285844f9b2".decode('hex'),
    "93eb19ccfa70f9c344fb78c17c3162f9a6a07e".decode('hex'),
    "89ef458def3bee865bf761c2753323f6b4b47cac01a3ab7f4bf77483516f6a364353e1ec20273d3fa718c724900e3ab4e28eca470e8b4e".decode('hex'),
    "aecd6386fa5cb99573f353d37e2877d88d970aca3fa6e62f08b14b81664122006e0cd6cf54100a378d49fa5ebf5c35afcdf993400dba2ec756af3b965dac76d645adf80a".decode('hex'),
    "81e3418dbb73ed915ced35d3783464feffa531fe03eaac7705ea31c7516f3f665454ebec20283923bf0acd6f860171a1f3cf865f088c079747a73b9166a01b8b4692f0560d1ea4026c58ff491447".decode('hex'),
]

plain = [
    "Hey Sariel apa kau membawa pesannya?",
    "Ya, aku membawanya.",
    "Cepat beritahu aku, kita tidak punya banyak waktu lagi.",
    "(Merlin menjelaskan, dia tidak mengerti kalimat ini karena terlalu rumit)",
    "Kita harus pergi dari sini, aku bisa merasakan ada yang sedang mengawasi kita.",
]

from pwn import xor
from Crypto.Cipher import ARC4

key = xor(cipher[4], plain[4])
print xor(cipher[3], key)