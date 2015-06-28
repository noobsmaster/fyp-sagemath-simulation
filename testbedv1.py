#generate all possible message of a message length in a list, in form column vector
def message_generation(msg_length):
	message_length=msg_length
	message_length=3
	no_msg=2**msg_length	 #number of message
	
	m_list = [list(("{0:0%db}"%message_length).format(m)) for m in range(no_msg)]
	m_mat_list = [matrix(GF(2),m) for m in m_list ]
	t_m_list=[m_mat_list[m].transpose() for m in range(no_msg)]
	return t_m_list

def random_between(j , k):
	a = int( random()*(k-j+1) )+ j
	return a
		
#random row generation, the generation is on demand, rather then generating whole matrix before hand
def rand_gene_generation(msg_length):
	return random_matrix(GF(2), 1, msg_length)		#1row x l-column

#generate 1 column of random sym for msg randomize purpose	
def rand_msg_generation(msg_length):
	return random_matrix(GF(2), msg_length, 1)		#nrow x 1column 
	
#random selection of rx data
def rand_selection_kplus10(k,tx_list_gen, tx_list_msg):
	tx_pool_no = len(tx_list_gen)
	tx_pool_list= [m for m in range(tx_pool_no)]
	chosen_list = []
	no_element_chosen = 0
	while no_element_chosen < k+10 :
		rand_choose = random_between(0, tx_pool_no-1 )
		chosen_list.append( tx_pool_list.pop(rand_choose))
		no_element_chosen += 1
		tx_pool_no -= 1
	
	#rx_mat_gen=
	rx_list_gen = [ tx_list_gen[m] for m in chosen_list]
	rx_list_msg = [ matrix(GF(2),tx_list_msg[m]) for m in chosen_list]
	
	return rx_list_gen, rx_list_msg

#Gaussian elimination
#1. search for row starts with 1 in 1st column, exchange with 1st row
#2. XOR/ADD row that starts with 1 in 1st column, 
#3. 
#decompose a binary matrix, with separate list for generator and encoded msg
#to acquire decoded msg

#row operation functions, xor and exchange
def row_ops (in_matrix, source_i, des_i, mode): 
	
	if mode == 'ex': #exchange mode, swaps row
		
		
		row_op_temp = in_matrix[source_i]
		in_matrix[source_i] = in_matrix[des_i]
		in_matrix[des_i] = row_op_temp
		
		return in_matrix
		
	if mode == 'xor' :	#xor operation mode, des=des xor source
		in_matrix[des_i] = in_matrix[des_i]+in_matrix[source_i]
		
		return in_matrix
	
#reducing matrix to triangular form, separate list for generator and message
def triangle_mat_decompo(input_mat_gene, input_mat_msg):
	
	no_rows = len(input_mat_gene)  #number of rows of mat
	no_cols = input_mat_gene[0].ncols() #number of columns of mat
	
	for pivot in range(no_cols):
		
		#note: possible improvement, instead scanning until bottom, scan until encounter a pivot
		# identify rows with pivot at [pivot] column 
		pivot_rows = []
			
		for i in range(pivot, no_rows):
						
			if input_mat_gene[i].column(pivot) != 0:
				pivot_rows.append(i)
				
						
		if len(pivot_rows) == 0: 	#fail to find pivot, decoding fails.
			 
			break
			
		#putting the first pivot rows to the top
		if pivot_rows[0] != pivot :
			
			input_mat_gene = row_ops(input_mat_gene, pivot, pivot_rows[0], 'ex')
			input_mat_msg = row_ops(input_mat_msg, pivot, pivot_rows[0], 'ex')
		
		del pivot_rows[0]
		
		
		#clearing values in [pivot] column below the [pivot] row
		while len(pivot_rows) != 0:
			i=pivot_rows[0]
			
			if pivot == (no_cols-1): 	break	# the triangle matrix has been formed, no point continuing
			
			
			input_mat_gene= row_ops(input_mat_gene, pivot, i, 'xor')
			input_mat_msg = row_ops(input_mat_msg, pivot, i, 'xor')
			
			del pivot_rows[0]
						
	if pivot == (no_cols-1):
		del	input_mat_gene[no_cols:no_rows]  #removing bottom part of matrix
		del input_mat_msg[no_cols:no_rows] 	#^^
	
	return input_mat_gene, input_mat_msg
	
#solve triangular matrix into identity matrix, and thus decode the message
def solve_triangular_matrix(in_mat_gene, in_mat_msg):
	
	no_rows = len(in_mat_gene)  #number of rows of mat
	no_cols = in_mat_gene[0].ncols() #number of columns of mat
	
	for i in range(no_rows):		
		
		if i == no_rows:
			break   #cant continue with last row
		
		for j in range( i+1, no_cols ):
			
			if in_mat_gene[i].column(j) != 0:  #	j > i, pivot value wont be affected
				
				in_mat_gene = row_ops(in_mat_gene, j, i, 'xor')
				in_mat_msg = row_ops(in_mat_msg, j, i, 'xor')
				
	return in_mat_gene, in_mat_msg	

#main function
def main(debug_opt=0):
	msg_length = 5
	k = msg_length 
	msg_mat = rand_msg_generation(k)
	tx_list_gene=[]
	tx_list_msg =matrix(GF(2), k+30, 1)
		
	for i in range(k+30):
		gene=rand_gene_generation(k)
		coded_msg= gene*msg_mat
		tx_list_gene.append(gene)
		tx_list_msg[i]=coded_msg
		tx_list_msg.transpose()
	
	if debug_opt==1 : print("tx_gen\n %s" %(tx_list_gene))
	if debug_opt==1 : print("tx_msg\n %s" %(tx_list_msg))
	
	
	rx_list_gene,rx_list_msg = rand_selection_kplus10(k,tx_list_gene, tx_list_msg)
	
	if debug_opt==1 : print("rx_gen\n %s" %(rx_list_gene))
	if debug_opt==1 : print("rx_msg\n %s" %(rx_list_msg))
				
	tri_mat_gene,tri_mat_msg= triangle_mat_decompo(rx_list_gene, rx_list_msg)
	
	if debug_opt==1 : print("tri_gen\n %s" %(tri_mat_gene))
	if debug_opt==1 : print("tri_msg\n %s" %(tri_mat_msg))
		
	iden_mat_gene,decode_msg= solve_triangular_matrix(tri_mat_gene, tri_mat_msg)

	if debug_opt==1 : print("identi_gen\n %s" %(iden_mat_gene))
	if debug_opt==1 : print("decode_msg\n %s" %(decode_msg))
	
	#change data format for ori_msg to match of decode_msg
	ori_msg=[ matrix(GF(2),msg_mat[i]) for i in range(msg_length)]
	
	if debug_opt==1 : print("ori\n %s" %(ori_msg)) 
	
	#check if decode_msg = ori_msg
	if decode_msg == ori_msg:
		if debug_opt==1 : print("decode success")
		return True
		
	else:
		if debug_opt==1 : print("decode fail")
		return False

failure = 0		
for rpt_i in range(10000):
		
	result = main()
	if result == False :
		failure +=1
		print ("fail")
	if rpt_i==1000 :
		print ("milestone 1")

print failure
	
	
	
	
	
	
	