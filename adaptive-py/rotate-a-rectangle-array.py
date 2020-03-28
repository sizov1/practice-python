def print_row(row):
	for elem in row:
		print(elem, end=" ")

def print_matirx(mt):
	for row in mt:
		print_row(row)
		print()

def rotate_matrix(matrix, n, m):
	res = []
	for i in range(m):
		res_row = []
		for row in matrix:
			res_row.append(row[i])
		res_row.reverse()
		res.append(res_row)
	return res


dim = [int(i) for i in input().split()]
n, m = dim[0], dim[1]
A = []

for i in range(n):
	row = [int(i) for i in input().split()]
	A.append(row[:m])

print_matirx(rotate_matrix(A, n, m))
