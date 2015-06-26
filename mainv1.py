#generate all possible message of a message length in a list, in form column vector
def message_generation(msg_length):
	message_length=msg_length
	message_length=3
	no_msg=2**msg_length	 #number of message
	
	m_list = [list(("{0:0%db}"%message_length).format(m)) for m in range(no_msg)]
	m_mat_list = [matrix(GF(2),m) for m in m_list ]
	t_m_list=[m_mat_list[m].transpose() for m in range(no_msg)]
	return t_m_list

#random row generation, the generation is on demand, rather then generating whole matrix before hand
def random_mat_generation(msg_length):
	return random_matrix(GF(2), 1, msg_length)		#1row x l-column

#generate 1 column of random sym for msg randomize purpose	
def random_msg_generation(msg_length):
	return random_matrix(GF(2), length, 1)		#nrow x 1column 
	
#random selection of rx data
def rand_selection_kplus10(k,tx_list):
	tx_pool_no = len(tx_list)
	tx_pool_list = [0: tx_pool_no-1 ]
	chosen_list = []
	no_ele_chosen = 0
	while no_ele_chosen < k+10
		rand_choose = random_between(0, tx_pool_no-1)
		chosen_list.append( tx_pool_list.pop[rand_choose])
		no_element_chosen++
		tx_pool_no--
	
	rx_list = [ tx_list[m] for m in chosen_list]
	return rx_list	

#Gaussian elimination
#1. search for row starts with 1 in 1st column, exchange with 1st row
#2. XOR/ADD row that starts with 1 in 1st column, 
#3. 
#// check with gaussian row operations methods

