from Crypto.Util.number import getPrime
import random
from secret import flag
import binascii

def generate_n():
	lis_prima = []
	while len(lis_prima) < 99:
		tmp = getPrime(512)
		if tmp not in lis_prima:
			lis_prima.append(tmp)

	lis_n = []

	for i in range(0, len(lis_prima)-1, 2):
		p = lis_prima[i]
		q = lis_prima[i+1]
		n = p*q
		lis_n.append(n)

	rand = random.randint(0, 97)
	lis_n.append(lis_prima[rand] * lis_prima[98])
	random.shuffle(lis_n)
	return lis_n

def generate():
	m = int(binascii.hexlify(flag), 16)
	e = 65537
	lis_n = generate_n()
	return m, e, lis_n

def biasalah_rsa(m, e, n):
	return pow(m, e, n)

def main():
	m, e, n = generate()
	enc = []
	for i in range(len(n)):
		enc.append(biasalah_rsa(m, e, n[i]))

	f = open('out.txt', 'w')
	f.write('''n : {},
e : {},
c : {}
'''.format(n, e, enc))
	f.close()

if __name__ == "__main__":
	main()

