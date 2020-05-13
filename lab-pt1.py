from tkinter import *
from tkinter.ttk import *
from math import *
from scipy.stats import chi2
import numpy as np
import matplotlib.pyplot as plt

root = Tk()
root.title('Моделирование случайной величины')
root.geometry("1000x950")
#root.resizable(False, False)

photo = PhotoImage(file = r"D:\\education\\kids-codes\\py\\pt1.png")   
Label(root, image=photo).grid(row=0, column=0, columnspan=7) 

#--Functions---#
def inverseF(y, p):
	return (1 / p) * np.log(1 / (1 - y))

def MyF(x):
	return len(vs[vs <= x]) / len(vs)

def f(x, k):
	return k*np.exp(-k*x)

def F(x, k):
	return 1.0 - np.exp(-k*x)
#--------------#

#---Main-expriment---#
def experiment():
	a = np.ones(len(params))
	for i in range(len(params)):
		a[i] = inverseF(np.random.random(), params[i])
	return np.min(a)

def serial_experiment():
	vs = []
	N = int(entry_N.get())
	for i in range(N):
		vs.append(experiment())
	return vs

def init_table():
	cols = ('i','x_i', 'exact_x_i')
	table = Treeview(root, selectmode='browse', columns=cols, show='headings')
	vsb = Scrollbar(orient="vertical", command=table.yview)
	table.configure(yscrollcommand=vsb.set)
	exact_values = np.sort(np.random.exponential(1 / sum(params), int(entry_N.get())))
	for col in cols:
		table.heading(col, text=col)
	if len(vs) >= 100:
		hi = np.linspace(0, len(vs) - 1, 100, dtype=int)
		for i in hi:
			table.insert("", "end", values=(i, vs[i], exact_values[i]))
	else:
		for i in range(len(vs)):
			table.insert("", "end", values=(i, vs[i], exact_values[i]))
	table.grid(row=15, column=0, columnspan=2, rowspan=5)
	vsb.configure(command=table.yview)

def go():
	if len(params) == 0:
		print("Параметры не заданы")
		return
	else:
		global vs 
		tmp = np.sort(serial_experiment())
		vs = tmp
		n = len(vs)
		k = sum(params)
		metrics = calculate_metrics(n, k)
		init_table()
		chi_squared_test(k)		
		metrics_table.insert("", "end", values=(metrics))

def intervals_chi_squared(s, k):
	z = np.ones(s - 1)
	for i in range(s - 1):
		z[i] = -np.log((s - 1 - i) / s) / k
	return z
	
def chi_squared_test(k):
	N = len(vs)
	s = int(entry_s.get())
	if (s < 1):
		return
	
	z = intervals_chi_squared(s, k)
	p = np.ones(s) * (1 / s)
	R0 = 0
	for j in range(s - 2):
		nj = len(vs[np.logical_and(vs >= z[j], vs < z[j+1])])
		R0 += (nj - N*p[j]) * (nj - N*p[j]) / (N * p[j])
		
	alpha = float(entry_alpha.get())
	critic_value = 1 - chi2.cdf(x=R0, df=(s - 1))

	pi_str = "Теоретические вероятности q = ["
	for pi in p:
		pi_str += " " + str(round(pi, 3)) + ","
	pi_str += "]"
	chi2_str = "1 - F(R0) = " + str(critic_value) + " -> "
	if (critic_value < alpha):
		chi2_str += "гипотеза о виде распределения отвергается"
	else:
		chi2_str += "гипотеза о виде распределения принимается"
	chi2_label = Label(root, text=chi2_str)
	pi_label = Label(root, text=pi_str)
	chi2_label.grid(row=10, column=0, columnspan=2)
	pi_label.grid(row=11, column=0, columnspan=2)

#--------------------#

#---Metrics---#
def median(n):
	if n == 1:
		return vs[0]
	elif n % 2 == 0:
		return (vs[n//2] + vs[n//2 + 1]) / 2
	else:
		return vs[(n+1)//2]

def calc_D(n,k):
	D = -99999.0
	for i in range(n):
		a = (i + 1) / n - F(vs[i], k)
		b = F(vs[i], k) - i / n
		c = max(a,b)
		if c > D:
			D = c
	return D

def calculate_metrics(n, k):
	E = 1/k
	x_  = np.sum(vs) / n
	dif_Ex = np.abs(E - x_)
	Disp = E * E
	s2 = np.sum((vs - x_) * (vs - x_)) / n
	dif_Ds2 = np.abs(Disp - s2)
	r_ = vs[n-1] - vs[0]
	Me = median(n)
	D = calc_D(n, k)
	return E, x_, dif_Ex, Disp, s2, dif_Ds2, Me, r_, D

def create_metrics_table():
	cols = ('E', '^x', '|E - ^x|', 'Dη', 'S^2', '|D - S^2|', '^Me', '^R', 'D')
	global metrics_table
	metrics_table = Treeview(root, selectmode='browse', column=cols, show='headings')
	for col in cols:
		metrics_table.heading(col, text=col)
		metrics_table.column(col, width=110)
	metrics_table.grid(row=8, column=0, columnspan=2, rowspan=2)
	vsb = Scrollbar(orient="vertical", command=metrics_table.yview)
	metrics_table.configure(yscrollcommand=vsb.set)
	vsb.configure(command=metrics_table.yview)	
#-------------#

#---Parameters-of-distribution---#
def init_params(entry_params, a):
	global params 
	tmp = np.fromstring(entry_params.get(), dtype=float, sep=' ')
	params = tmp
	a.destroy()
	return params

def input_params(k):
	a = Toplevel()
	a.title('Параметры распределений')
	a.geometry("650x70")

	lambda_entryes = []
	k = int(k)
	params = np.ones(k)

	label_params = Label(a, text="λ_i")
	entry_params = Entry(a, width=100)
	default_params = ""
	for i in range(k):
		random_parameter = np.random.uniform(0,1)
		params[i] = random_parameter
		default_params += str(random_parameter)[:4] + "  "
	entry_params.insert(0, default_params)
	entry_params.grid(row=0,column=1)
	label_params.grid(row=0,column=0, sticky=E)

	go_button = Button(a, text="Вперёд", command=lambda : init_params(entry_params, a))
	go_button.grid(row=k, column=0, columnspan=2, pady=10)
#--------------------------------#

#---Histogramm---#
def init_hist_table(hist_data):
	cols = ('x_i', 'f(x_i)', 'n_i / (n * l_i)')
	density_table = Treeview(root, selectmode='browse', columns=cols, show='headings')
	vsb = Scrollbar(orient="vertical", command=density_table.yview)
	density_table.configure(yscrollcommand=vsb.set)
	for col in cols:
		density_table.heading(col, text=col)
		density_table.column(col, width=90)
	for row in hist_data:
		density_table.insert("", "end", values=(row))
	vsb.configure(command=density_table.yview)
	mhd = max_difference_hist(hist_data)
	str_mhd = "max|f(x_i) - n_i / (n * l_i)| = " + str(mhd[1])
	str_mhd += " в точке " + str(round(mhd[0], 5))
	max_hist_label = Label(root, text=str_mhd)
	density_table.grid(row=12, column=0, columnspan=4)
	max_hist_label.grid(row=13, column=0, columnspan=2, rowspan=2)

def draw_bar_for_hist(yi, a, b):
	y = np.ones(100) * yi
	x = np.linspace(a, b, 100)
	l1 = plt.plot(x, y, linewidth=1.5, color = "r")
	x = np.ones(100) * b
	y = np.linspace(yi, 0, 100)
	l1 = plt.plot(x, y, linewidth=1.5, color = "r")
	x = np.ones(100) * a
	l1 = plt.plot(x, y, linewidth=1.5, color = "r")

def max_difference_hist(hist_data):
	res, xres = 0, 0
	for row in hist_data:
		val = np.abs(row[1]-row[2]) 
		if val > res:
			xres = row[0]
			res = val
	return xres, res
	
def draw_user_hist(ui, entry_intervals):
	intervals = [i for i in entry_intervals.get().split()]
	li = len(intervals)
	n = len(vs)
	ui.destroy()
	y_data = np.ones(li-1)
	x_data = np.ones(li-1)
	hist_data = []
	k = sum(params)
	for i in range(li-1):
		a, b = float(intervals[i]), float(intervals[i+1])
		values = vs[vs>a]
		values = values[values<=b]
		zi = a + (b - a) / 2 
		ni = len(values)
		yi = ni / (n * (b - a))
		row = zi, f(zi, k), yi
		hist_data.append(row)
		draw_bar_for_hist(yi, a, b)
	x_value = np.linspace(float(intervals[0]), float(intervals[li-1]), 1000)
	y_value = f(x_value, k)
	l = plt.plot(x_value, y_value, linewidth=1.5, color="b")
	init_hist_table(hist_data)
	plt.show()

def draw_unif_hist(ui, entry_a, entry_b, entry_s):
	a = float(entry_a.get())
	b = float(entry_b.get())
	s = int(entry_s.get())	
	ui.destroy()
	k = sum(params)
	n = len(vs)
	hist_data = []
	values = vs[vs > a]
	values = values[values <= b]
	nb, bins, patches = plt.hist(values, s, density=True, facecolor='r', alpha=0.8)
	xi, step = np.linspace(a, b, s, retstep=True)
	for i in range(s-1):
		zi = xi[i] + (xi[i+1] - xi[i]) / 2
		values = vs[vs>xi[i]]
		values = values[values<=xi[i+1]]
		ni = len(values)
		row = zi, f(zi, k), ni/(n*step)
		hist_data.append(row)
	x_value = np.linspace(a, b, 1000)
	y_value = f(x_value, k)
	l = plt.plot(x_value, y_value, linewidth=1.5, color="b")
	init_hist_table(hist_data)
	plt.show()
#----------------#

#---Intervals-for-histogramm---#
def user_intervals(abi):
	abi.destroy()
	ui = Toplevel()
	ui.title('Интервалы гистрограммы')
	ui.geometry("300x300")
 
	label_intervals = Label(ui, text="Введите границы интервалов через пробел")
	entry_intervals = Entry(ui)
	butt_draw = Button(ui, text="Вперёд", command=lambda:draw_user_hist(ui, entry_intervals))

	label_intervals.grid(row=0, column=0)
	entry_intervals.grid(row=1, column=0)
	butt_draw.grid(row=2, column=0)

def uniform_intervals(abi):
	abi.destroy()
	ui = Toplevel()
	ui.title('Интервалы гистрограммы')
	ui.geometry("375x100")

	label_a = Label(ui, text="Правая граница a = ")
	label_b = Label(ui, text="Левая граница b = ") 
	label_s = Label(ui, text="Число разбиений гистрограммы nbins = ") 
	entry_a = Entry(ui)
	entry_b = Entry(ui)
	entry_s = Entry(ui)
	butt_draw = Button(ui, text="Вперёд", width=40, command=lambda:draw_unif_hist(ui, entry_a, entry_b, entry_s))

	label_a.grid(row=1, column=0, sticky=E)
	label_b.grid(row=2, column=0, sticky=E)
	label_s.grid(row=3, column=0, sticky=E)
	entry_a.grid(row=1, column=1)
	entry_b.grid(row=2, column=1)
	entry_s.grid(row=3, column=1)
	butt_draw.grid(row=4, column=0, columnspan=2)

def ask_about_intervals():
	abi = Toplevel()
	abi.title('Интервалы для гистрограммы')
	abi.geometry("250x100")

	butt_uniform_intervals = Button(abi, text="Равномерные интервалы на отрезке", command=lambda:uniform_intervals(abi), width=40)
	butt_user_intervals = Button(abi, text="Задать интервалы в ручную", width=40, command=lambda:user_intervals(abi))

	butt_uniform_intervals.grid(row=0, column=0, pady=10)
	butt_user_intervals.grid(row=2, column=0, pady=10)

def calc_taks_taks():
	for i in range(1000):
		go()
	list_D = np.array([])
	l = 1.224
	for line in metrics_table.get_children():
		list_D = np.append(list_D, float(metrics_table.item(line)['values'][3]))
	print(list_D)
	ni = len(list_D[list_D>l])
	print(ni/len(metrics_table.get_children()))
#------------------------------#

#---Draw-CDF---#
def draw_cdf():
	n = len(vs)
	a, b = vs[0], vs[n - 1]
	k = sum(params)

	ex_value = np.linspace(a, b, 1000)
	ey_value = F(ex_value, k)
	l_exact = plt.plot(ex_value, ey_value, color="b")

	if n < 500:
		for i in range(n - 1):
			myx_value = np.linspace(vs[i], vs[i+1], 1000)
			myy_value = np.ones(1000) * MyF(vs[i+1])
			l = plt.plot(myx_value, myy_value, color="r")
	else:
		myx_value = ex_value
		vecMyF = np.vectorize(MyF, otypes=[float])
		myy_value = vecMyF(myx_value)
		l = plt.plot(myx_value, myy_value, color="r")
	plt.show()

label_input = Label(root, text="\nВходные данные")
label_input.grid(row=1, column=0, columnspan=2)

label_k = Label(root, text="Число мужчин k = ")
label_N = Label(root, text="Число экспериментов N = ")
label_s = Label(root, text="Число интервалов для критерия согласия s = ")
label_alpha = Label(root, text="Уровень значимости α = ")

label_k.grid(row=2, column=0, sticky=E)
label_N.grid(row=3, column=0, sticky=E)
label_s.grid(row=4, column=0, sticky=E)
label_alpha.grid(row=5, column=0, sticky=E)

entry_k = Entry(root)
entry_N = Entry(root)
global entry_s 
entry_s = Entry(root)
global entry_alpha 
entry_alpha = Entry(root)

entry_k.grid(row=2, column=1, sticky=W)
entry_N.grid(row=3, column=1, sticky=W)
entry_s.grid(row=4, column=1, sticky=W)
entry_alpha.grid(row=5, column=1, sticky=W)

params_button = Button(root, text="Задать параметры", command=lambda:input_params(entry_k.get()))
params_button.grid(row=6, column=0, pady=10)

button = Button(root, text="Запустить", command=go)
button.grid(row=6, column=1, pady=10)

draw_button = Button(root, text="Нарисовать гистрограмму", command=lambda:ask_about_intervals())
draw_button.grid(row=7, column=1, pady=10)

create_metrics_table()
#calc_butt = Button(root, text="Проверка", command=lambda:calc_taks_taks())
#calc_butt.grid(row=6, column=0, pady=10)

cdf_button = Button(root, text="Нарисовать ФР", command=lambda:draw_cdf())
cdf_button.grid(row=7, column=0, pady=10)
root.mainloop()

