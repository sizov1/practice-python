t = input()

if t == "triangle":
	a = float(input())
	b = float(input())
	c = float(input())
	p = (a + b + c) / 2
	s2 = p * (p - a) * (p - b) * (p - c)
	print(pow(s2, 0.5))
elif t == "circle":
	a = float(input())
	pi = 3.14
	print(a*a*pi)
elif t == "rectangular":
	a = float(input())
	b = float(input())
	print(a * b)