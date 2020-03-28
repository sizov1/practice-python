
import numpy as np
import csv

number_of_servers = 3
number_of_stages = 2

states = np.array([[0,0,0,0], [0,1,1,0], [0,1,0,1], [1,1,0,0], [0,2,2,0],
	              [0,2,1,1], [1,2,1,0], [0,2,0,2], [1,2,0,1], [2,2,0,0],
	              [0,3,3,0], [0,3,2,1], [1,3,2,0], [0,3,1,2], [1,3,1,1],
	              [2,3,1,0], [0,3,0,3], [1,3,0,2], [2,3,0,1], [3,3,0,0],
	              [0,4,3,0], [0,4,2,1], [1,4,2,0], [0,4,1,2], [1,4,1,1],
	              [2,4,1,0], [0,4,0,3], [1,4,0,2], [2,4,0,1], [3,4,0,0],
	              [0,5,3,0], [0,5,2,1], [1,5,2,0], [0,5,1,2], [1,5,1,1],
	              [2,5,1,0], [0,5,0,3], [1,5,0,2], [2,5,0,1], [3,5,0,0]])

def get_state_name(state):
	row = ""
	for i in range(len(state)):
		row += str(state[i])
	return row

def only_one_operation(state_i, state_j):
	sb = state_j - state_i

	if np.count_nonzero(sb) > 2:
		return False

	if not np.all(np.abs(sb) <= 1):
		return False

	return True

def is_end_serve(state_i, state_j):
	sb = state_j - state_i


	if sb[1] != -1 or state_i[0] == 0:
		return False
	
	#second case
	if np.count_nonzero(state_i[2:]) == 0 and sb[0] == -1:
		return True	

	if sb[0] == 0:
		#thirty case
		if np.count_nonzero(sb[2:]) == 0 and state_i[1] > number_of_servers:
			return True
		#4th case
		ind = np.where(state_i[2:] != 0)[0][0]
		print("state_i = ", state_i)
		print("state_j = ", state_j)
		print("ind = ", ind)
		if state_j[2:][ind] != state_i[2:][ind]:
			return True

	return False

def self_intense(state):
	row = ""
	row += '-(l'
	if state[0] != 0:
		row += ' + ' + str(state[0]) + 'm'				
	if np.sum(state[2:]) != 0:
		row += ' + ' + str(np.sum(state[2:])) + 'a'
	row += ")"
	return row

def is_new_request(state_i, state_j):
	sb = state_j - state_i

	if np.count_nonzero(sb) > 2:
		return False

	if sb[1] == 1:
		if sb[2] == 1:
			return True
		if np.count_nonzero(sb) == 1:
			return True

def init_intense_matrix(states):
	n_states = len(states)

	mt = np.chararray((n_states, n_states), itemsize=14,unicode=True)

	with open('mt.csv', 'w', newline='') as csvfile:
		Q = csv.writer(csvfile, delimiter=';',
	                            quotechar=' ', quoting=csv.QUOTE_MINIMAL)

		header_row = " ;"
		for i in range(n_states):
			header_row += get_state_name(states[i])
			header_row += ";"
		Q.writerow([header_row])

		for i in range(n_states):
			row = ''
			row += get_state_name(states[i]) + ";"
			for j in range(0, n_states):

				sb = states[j] - states[i] # разница векторов состояний
				nsbnz = np.count_nonzero(sb)

				# за один переход завершилось более 2ух операций
				if not only_one_operation(states[i], states[j]):
					row += '0;'
					continue

				if i == j:	
					# интенсивность перехода состояния в себя
					row += self_intense(states[i]) + ";"
					continue

				if is_new_request(states[i], states[j]):
					# поступление требования 
					row += 'l'
				elif is_end_serve(states[i], states[j]):
					# завершения обслуживания
					#print(states[i], states[j], np.where(sb[2:] != 0)[0])
					mval = states[i][0]
					if mval == 1:
						row += 'm'
					else:
						row += str(states[i][0]) + 'm'
				elif sb[1] == 0 and i < j:
					inzeosb = np.nonzero(sb)[0]
					if abs(inzeosb[1] - inzeosb[0]) > 1 and inzeosb[1] == 3:
						# переход с последней фазы разогрева на обслуживание 
						aval = states[i][np.where(sb < 0)[0][0]]
						if aval == 1:
							row += 'a'
						else:
							row += str(states[i][np.where(sb < 0)[0][0]]) + 'a'	
					if abs(inzeosb[1] - inzeosb[0]) == 1:
						# переход с одной фазы разогрева на другую
						aval = states[i][np.where(sb < 0)[0][0]]
						if aval == 1:
							row += 'a'
						else:
							row += str(states[i][np.where(sb < 0)[0][0]]) + 'a'	
				else:
					row += '0'

				row += ';'	
			Q.writerow([row])
	    

init_intense_matrix(states)