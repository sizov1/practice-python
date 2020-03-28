import numpy as np
import math
import random as random
import matplotlib.pyplot as plt

k = 1.74
g = 10.0
Em = 121.656
H = 6.0

def f1(v_n):
	return k * k * v_n

def f2(v_n):
	return np.abs(k * k * v_n - 2 * k * k * Em)

def f(v_n):
	if v_n < 2 * g * H:
		return f1(v_n)
	else:
		return f2(v_n)

def on_bis(x, y, c):
	xi = np.linspace(y, x, 1000)
	yi = np.ones(1000) * y
	ob = plt.plot(xi, yi, linewidth=1.5, color=c)

def on_f1(x, c):
	xi = np.ones(1000) * x
	yi = np.linspace(x, f1(x), 1000)
	of1 = plt.plot(xi, yi, linewidth=1.5, color=c)


def on_f2(x,c):
	xi = np.ones(1000) * x
	yi = np.linspace(x, f2(x), 1000)
	of2 = plt.plot(xi, yi, linewidth=1.5, color=c)

def on_f(x,c):
	if x < 2 * g * H:
		on_f1(x,c)
	else:
		on_f2(x,c)

def throw_ball(n_steps, v0):
	for i in range(n_steps):
		v1 = f(v0)
		on_bis(v0, v1, "b")
		on_f(v1, "b")
		
		#	on_bis(v0, v1, "y")
		#	on_f(v1, "y")

		v0 = v1


x1 = np.linspace(0, 2 * g * H, 1000)
x2 = np.linspace(2 * g * H, 600, 5000)
x = np.linspace(0, 600, 5000)

y1 = f1(x1)
y2 = f2(x2)

l1 = plt.plot(x1, y1, linewidth=1.5, color = "r")
l2 = plt.plot(x2, y2, linewidth=1.5, color = "r")
l = plt.plot(x, x, linewidth=1.5, color = "g")

v0 = (2 * k ** 2 * (1 - k**4) * Em) / (1 - k**6) 
plt.scatter(v0, f(v0), marker="*")
throw_ball(20, v0)

print((k**2 * v0 - 2 * k ** 2 * Em) > 2 * g * H)  
print(k**2 * (v0 - 2 * Em) - 2 * Em < 0)

plt.plot()
plt.show()
