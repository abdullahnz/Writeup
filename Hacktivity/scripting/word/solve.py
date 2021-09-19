
maps = [
    'DYOUPFKUIIBJCFGS',
    'BCVXTEWLQDVRQRGR',
    'MYLMKXHOZYKLDHPG',
    'ENMESBTVPRPASZYA',
    'UYEUMOACOXAEVNRD',
    'SWEATYLTGPVOHPHA',
    'ZTSHTXZLHMJATRRF',
    'BLKSCQKAIRVYYAUY',
    'QHXFZKBRQLOXNSWS',
    'TASZMSFATSNBPWHX',
    'EVEWLZLVNUATEUGW',
    'SRZBSIKAWDPXZSLY',
    'JGSOPZGVVGYDJZAL',
    'PAPNSOVNLELGXFHN',
    'HGBZQLNCOBXAXJGE',
    'OLPHHHJVGIHLUCVB',
]

STEP = [
    (-1,  0), (1,  0),
    ( 0, -1), (0,  1),
    (-1, -1), (1,  1),
    (-1,  1), (1, -1)
]

def check(words, pos):
    calculated = ''  
    for x, y in pos:
        calculated += maps[x][y]
    if calculated == words:
        return True
    return False

def recursive(words, index, pos, step=()):
    if index == len(words):
        return check(words, pos)

    pos_x = (pos[-1][0] + step[0])
    pos_y = (pos[-1][1] + step[1])

    if pos_x > 15:
        pos_x -= 15
    
    if pos_y > 15:
        pos_y -= 15
    
    if maps[pos_x & 15][pos_y & 15] == words[index]:
        pos.append((pos_x, pos_y))
        return recursive(words, index + 1, pos, step = step)
    
    return False

def find_start_move(char):
    result = []
    for x in range(0x10):
        for y in range(0x10):
            if maps[x][y] == char:
                result.append((x, y))
    return result

def search(words):
    start_movement = find_start_move(words[0])
    for start in start_movement:
        for step in STEP:
            pos   = [start]
            index = 1
            if recursive(words, index, pos, step = step):
                return [p[::-1] for p in pos]

def get_maps():
    r.recvlines(3)
    maps = []
    for i in range(0x10):
        line = b''.join(r.recvline(0).split()[2:])
        maps.append(line.decode())
    r.recvlines(2)
    return maps

from pwn import *

HOST = 'challenge.ctf.games'
PORT = 30433

if __name__ == '__main__':
    r = remote(HOST, PORT)
    
    r.sendlineafter('> ', 'play')
    
    for level in range(30):
        t = log.progress(f'Level #{level + 1}')
        maps = get_maps()
        
        for _ in range(5):
            word = r.recvuntil(b':', drop = True)
            ans  = search(word.decode())

            t.status(f'\n{word}: {ans}' )
            r.sendlineafter('> ', f'{ans}')
        
        t.success(r.recvlines(3)[0].decode())

    r.interactive()

# maps = [
#     'SXJRGOMVROWAKLRF',
#     'VNCBVQNNPJPVCTRC',
#     'EBCFCOEZFRSSOKCN',
#     'YOPTJFEAZNGUPKLX',
#     'GOROXMORDEREDQAK',
#     'GKICQOLIWSCJKMRK',
#     'XMFCSVBNJRSYOXID',
#     'QOPWQSJGCFVUNENJ',
#     'IBRETINUEWPNHWEN',
#     'SIBWXQOAJZNERCTS',
#     'JLUHOEZQAYAHMUTQ',
#     'EEJWCMAAXPAWHLIZ',
#     'OSLGPHEYSDKWKPSK',
#     'JBMQAUMNTXEVKUTN',
#     'ZNHCDARDDOFEMCSJ',
#     'JVZMMLWLBWLXPYCY',
# ]


# HEAP = [(12, 8), (11, 9), (10, 10), (9, 11), (8, 12)]

# print(search('HEAP'))
# print(recursive('HEAP', 1, pos, step = (1, -1)))

# print(search('HEAP'))

# SWEATY    = [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5)]
# SLAVE     = [(5, 9), (6, 10), (7, 11), (8, 12), (9, 13)]
# BATHROBES = [(5, 3), (6, 4), (7, 5), (8, 6), (9, 7), (10, 8), (11, 9), (12, 10), (13, 11)]
# PULL      = [(12, 9), (13, 10), (14, 11), (15, 12)]
# BANDY     = [(6, 8), (7, 9), (8, 10), (9, 11), (10, 12)]

# print(search('SWEATY'))
# print(SWEATY)
# print('---')
# print(search('SLAVE'))
# print(SLAVE)
# print('---')
# print(search('BATHROBES'))
# print(BATHROBES)
# print('---')
# print(search('PULL'))
# print(PULL)
# print('---')
# print(search('BANDY'))
# print(BANDY)

