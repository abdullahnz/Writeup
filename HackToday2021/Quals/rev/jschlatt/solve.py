'''
main:
    print jambo(13) + jambo(37)

jambo:
    - arg
    if arg <= 1:
        return arg

    b = 0
    c = 0

    if c < arg:
        b += jambo(c) * jambo(arg - c - 1) 
        c += 1
    else:
        return b
'''

cache = []

def jambo(n):
    global cache

    if n <= 0:
        return 1
    
    if n < len(cache):
        return cache[n]

    # x = 0
    # y = 0

    # while y < n:
    #     x += jambo(y) * jambo(n - y - 1)
    #     y += 1
     
    x = 0
    for i in range(n):
        x += jambo(i) * jambo(n - i - 1)
    
    cache += [x]
    return cache[-1]

if __name__ == "__main__":
    ans = jambo(13) + jambo(37)
    print(f'hacktoday{{{ans}}}')
    