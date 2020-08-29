from z3 import *

s = Solver()
key = [BitVec('key{}'.format(i), 32) for i in range(4)]

flag = [[50, 11, 18, 12], [18, 12, 23, 2], [21, 11, 35, 42], [47, 2, 12, 40]]
target = [7681, 4019, 7160, 8080]

for i in range(4):
	s.add(key[i] <= 255, key[i] >= 0 )
	
s.add( 
	(key[0]*flag[0][0]) +
	(key[1]*flag[0][1]) +
	(key[2]*flag[0][2]) +
	(key[3]*flag[0][3]) == 7681
)
s.add( 
	(key[0]*flag[1][0]) +
	(key[1]*flag[1][1]) +
	(key[2]*flag[1][2]) +
	(key[3]*flag[1][3]) == 4019
)
s.add( 
	(key[0]*flag[2][0]) +
	(key[1]*flag[2][1]) +
	(key[2]*flag[2][2]) +
	(key[3]*flag[2][3]) == 7160
)
s.add( 
	(key[0]*flag[3][0]) +
	(key[1]*flag[3][1]) +
	(key[2]*flag[3][2]) +
	(key[3]*flag[3][3]) == 8080
)

if s.check() == sat:
	m = s.model()
	keys = ''
	for k in key:
		    keys += chr(m[k].as_long())
	print keys
