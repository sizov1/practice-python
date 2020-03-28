fir﻿st_number = float(input())
second_number = float(input())
operation = input()

try:
    operations = {
            '+': first_number + second_number,
            '-': first_number - second_number,
            '*': first_number * second_number,
            'pow': first_number ** second_number,
            '/': first_number / second_number,
            'mod': first_number % second_number,
            'div': int(first_number // second_number),
        }
    print(operations[operation])
except ZeroDivisionError:
    operations = {
            '+': first_number + second_number,
            '-': first_number - second_number,
            '*': first_number * second_number,
            'pow': first_number ** second_number
        }
    if operation in ('/', 'div', 'mod'):
        print("Division by 0!")
    else:
        print(operations[operation])

"""
a = float(input())
b = float(input())
op = str(input())

if op == "-":
	print(a - b)
elif op == "+":
	print(a + b)
elif op == "*":
	print(a * b)
elif op == "/":
	if b != 0.0:
		print(a / b)
	else:
		print("Division by 0!") 
elif op == "mod":
	if b != 0.0:
		print(a % b)
	else:
		print("Division by 0!") 		
elif op == "pow":
	print(pow(a, b))
elif op == "div":
	if (b != 0.0):
		print(a//b)
	else:
		print("Division by 0!") 

"""