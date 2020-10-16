tab = [b'\x80\xa5',b'\xc7\xe3',b'\xf6\xff',b'\xfc\xee',b'\xd6\xb7',b'\x93\x6c',b'\x48\x29',b'\x11\x03',b'\x00\x09',b'\x1c\x38',b'\x5a\x80']

# s = '5249 4646 a4e3 0000 5741 5645 666d 7420 \n1000 0000 0100 0100 803e 0000 803e 0000\n0100 0800 6461 7461 803e 0000 '
# s = b'\x52\x49\x46\x46a4e3000057415645666d7420\n1000000001000100803e0000803e0000\n0100080064617461803e0000'

s = b'\x52\x49\x46\x46\xa4\xe3\x00\x00\x57\x41\x56\x45\x66\x6d\x74\x20\x10\x00\x00\x00\x01\x00\x01\x00\x80\x3e\x00\x00\x80\x3e\x00\x00\x01\x00\x08\x00\x64\x61\x74\x61\x80\x3e\x00\x00'

with open('s.wav', 'wb+') as f:
	f.write(s)
	f.write(tab[0])
	f.write(tab[1])
	# f.write('\n')

	for i in range(7998):
		f.write(tab[(i+2)%11])

		# if i%8 == 7:
			# f.write('\n')

f.close()