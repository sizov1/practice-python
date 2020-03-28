s = input().split()

a = int(s[0])
b = int(s[1])

for i in range(a, b + 1):
	out = ''
	if i % 3 == 0:
		out += "Fizz"
	if i % 5 == 0:
		out += "Buzz"
	if len(out) == 0:
		out += str(i)
	print(out)


