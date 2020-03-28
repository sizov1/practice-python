import numpy as np

n = int(input("Number of people = "))
niog = int(input("Number of groups = "))
if n % niog != 0:
	print("debil-debilich")
else:
	print("Input names across space")
	names = input().split()
	n = len(names)
	dic_names = { i : names[i] for i in range(n)}
	arr = np.arange(8)
	np.random.shuffle(arr)
	groups = []
	arrs = np.split(arr, niog)
	for array in arrs:
		group = []
		for j in array:
			group.append(dic_names[j])
		groups.append(group)
	for group in groups:
		print(group)
print("press any key")
a = input()