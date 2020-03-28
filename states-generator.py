import numpy as np

def get_finish_state(number_of_steps, number_of_request, number_of_servers):
	max_activity_servers = min(number_of_request, number_of_servers)
	finish_state = np.zeros(number_of_steps + 1, dtype=int)
	finish_state[-1] = max_activity_servers
	return finish_state

def next_state(state, r):
	indexs_of_nonzero_elem = np.nonzero(state)
	index_of_last_nonzero_elem = indexs_of_nonzero_elem[0][-1]
	if index_of_last_nonzero_elem == r:
		if state[r - 1] != 0:
			state[r - 1] = state[r - 1] - 1
			state[r] = state[r] + 1	
		else :
			almost_result = next_state(state[:r], r-1)	
			return np.append(almost_result, state[r])
	else:
		state[index_of_last_nonzero_elem] = state[index_of_last_nonzero_elem] - 1
		state[index_of_last_nonzero_elem + 1] = state[index_of_last_nonzero_elem + 1] + 1
	return state

def generate_state_space(c, r, s):
	state = np.zeros(r + 1, dtype=int)  #state[0] - number of servers on 1st step setup
										#state[1] - number of servers on 2nd step setup
										#...
										#state[r-1] - number of servers on r-1 step setup 
										#state[r] - number of active servers
	states = []		
	max_activity_servers = min(s, c)
	for request in range(1, max_activity_servers + 1):
		state = np.zeros(r + 1, dtype=int)
		state[0] = request
		finish_state = get_finish_state(r, request, c)
		while not np.all(state == finish_state):
			#print(state)
			states.append(state.tolist())
			state = next_state(state, r)
		states.append(state.tolist())

	n = len(states)
	for i in range(0, n):
		states[i].append(sum(states[i]))

	begining_inifinity = []
	for state in states:
		if state[-1] == c:
			begining_inifinity.append(state)
			
	for j in range(max_activity_servers + 1, s + 1):
		for state in begining_inifinity:
			state[-1] = state[-1] + 1
			states.append(state)
	
	return states
	

c = 3 #number of servers 
r = 2 #number of steps setup
s = 6 #number of request
generate_state_space(c, r, s)

