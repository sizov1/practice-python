numbers = [int(i) for i in input().split()]
n = len(numbers)

if n == 1:
	print(numbers[0])
else:
	nlon = [numbers[1] + numbers[n - 1]]
	for i in range(1, n - 1):
		nlon.append(numbers[i-1] + numbers[i+1])
	nlon.append(numbers[0] + numbers[n - 2])
	for i in nlon:
		print(i, end=" ")