from collections import Counter
import pprint

pp = pprint.PrettyPrinter(indent=4)

with open('marpaz.csv', 'r') as data:
	lines = data.readlines()

data.close()

stringi = []

l = []
setSources = set()
counts = dict()

for i in lines: #range(10):
	params = i.split(',')

	# line = ''
	# for j in range(2,8):
	# 	line += params[j] + ' '

	string = params[7]
	cash = float(params[3][1:-1])


	if string not in stringi:
		counts.update({string: 0})
	# if string.split(' ')[0] == "Data":
	# 	# print(params[6] + ' ' + params[7])
	# 	string = params[6]


	if cash > 0:
		print((params[0] + ' income :' + str(cash)))

	setSources.add(string)
	l.append([string, cash])
	stringi.append(string)

# print(counts)

income = 0
outcome = 0

for item in setSources:

	for key, value in l:
		if key == item:
			money = float(value)
			counts[item] += money

			if money > 0:
				income += money
			else:
				outcome += money

pp.pprint(sorted(counts.items(), key=lambda item: item[1], reverse=True))

print(('income: ' + str(income) + ' ; outcome: ' + str(outcome)))
# d = Counter(stringi)
# for key, value in d.most_common():
# 	print((str(value) + ' ' + key))
