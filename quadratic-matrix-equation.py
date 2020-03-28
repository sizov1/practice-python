import numpy as np
import csv

l, m, a = 0.4, 0.5, 0.7
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
	intense = -l
	intense = intense - state[0] * m				
	intense = intense - np.sum(state[2:]) * a
	return intense

def is_transition_into_layer(state_i,i,state_j, j):
	sb = state_j - state_i
	if sb[1] == 0 and i < j:
		inzeosb = np.nonzero(sb)[0]
		itil_flag = (abs(inzeosb[1] - inzeosb[0]) > 1 and inzeosb[1] == 3) or abs(inzeosb[1] - inzeosb[0]) == 1
		return itil_flag, inzeosb[0]
	return False, 0		

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

	mt = np.zeros((n_states, n_states))
	print(mt)
	for i in range(n_states):
		for j in range(n_states):
			if not only_one_operation(states[i], states[j]):
				mt[i][j] = 0.0	
			if i == j:
				mt[i][j] = self_intense(states[i])
			if is_new_request(states[i], states[j]):
				mt[i][j] = l
			elif is_end_serve(states[i], states[j]):
				mt[i][j] = states[i][0] * m
			else:
				itil = is_transition_into_layer(states[i], i, states[j], j)
				if itil[0]:
					mt[i][j] = itil[1]
	for i in range(n_states):
		for j in range(n_states):
			print("{:.2f}".format(mt[i][j]), end = " ")
		print("\n")

init_intense_matrix(states)