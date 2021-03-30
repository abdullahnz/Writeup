import struct, base64

enc = 'Fw1jaAgOZmESGHtqAWp0X2tdXzNOCnp5FjFvbl9rbDQAN2hfX30AAA=='.decode('base64')
a = []

for i in range(0, len(enc), 4):
    a.append(struct.unpack("I", enc[i:i+4])[0])

b = []
for c in a:
    b += [c ^ (c >> 16)]

print ''.join(map(lambda x: struct.pack("I", x), b))

