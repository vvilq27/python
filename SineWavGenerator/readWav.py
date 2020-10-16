import binascii

t = [0]*36
f = open('s.wav', 'rb')
for i in range(36):
	t[i] = binascii.hexlify(f.read(1))


print(t)
