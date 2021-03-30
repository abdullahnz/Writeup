import struct, base64
from secret import flag as ackerman

def ereh(mikasa):
	ereh = 4 - len(mikasa) % 4
	if ereh != 0:
		mikasa = mikasa + b"\x00" * ereh
	return mikasa

def jean(sasha):
	connie = struct.unpack("I" * (len(sasha) // 4), sasha)
	return connie

def titan(iegerist):
	ymir = []
	for ieger in iegerist:
		ymir += [ieger ^ (ieger >> 16)]
	return ymir

def attack(grisha, kruger):
	eldia = []
	for attack_titan in range(len(grisha)):
		eldia += [kruger[attack_titan] ^ (grisha[attack_titan] >> 16)]
	return eldia

def aliansi(hanji):
	squad = []
	for erwin in hanji:
		squad += [erwin ^ (erwin >> 16)]
	return squad

def rumbling(walls):	
	livai = b''
	for wall in walls:
		livai += struct.pack("I", wall)
	return base64.b64encode(livai)


hehe = str(rumbling(aliansi(attack(jean(ereh(ackerman)),titan(jean(ereh(ackerman)))))))

f = open("out.txt", "w")
f.write(hehe)
f.close()