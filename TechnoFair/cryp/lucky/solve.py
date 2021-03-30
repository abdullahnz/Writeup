cipher = open('cipher.txt').read().split('==')

for _ in range(7):
    a = ''
    for c in cipher:
        c = c + '=='
        a += c.decode('base64')
    cipher = a.split('==')

print a

