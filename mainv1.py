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
	
	rx_list_gen = [ tx_list_gen[m] for m in chosen_list]
	rx_list_msg = [ tx_list_msg[m] for m in chosen_list]
	
	return rx_list_gen, rx_list_msg

#Gaussian elimination
#1. search for row starts with 1 in 1st column, exchange with 1st row
#2. XOR/ADD row that starts with 1 in 1st column, 
#3. 
#decompose a binary matrix, with separate list for generator and encoded msg
#to acquire decoded msg

#row operation functions, xor and exchange
def row_ops (matrix, source_i, des_i, mode): 
	
	if mode == 'ex': #exchange mode, swaps row
		row_op_temp = []
		row_op_temp = matrix[source_i]
		matrix[des_i] = matrix[source_i]
		matrix[source_i] = row_op_temp
		
		return matrix
		
	if mode == 'xor' :	#xor operation mode, des=des xor source
		matrix[des_i] = matrix[des_i].__xor__(input_mat[pivot])
		
		return matrix
	
#reducing matrix to triangular form, separate list for generator and message
def triangle_mat_decompo(input_mat_gene, input_mat_msg):
	
	no_rows = len(input_mat_gene)  #number of rows of mat
	no_cols = len(input_mat_gene[0]) #number of columns of mat, assuming mat inserted is a rectangular mat
	
	for pivot in range(no_cols):
		
		#note: possible improvement, instead scanning until bottom, scan until encounter a pivot
		# identify rows with pivot at [pivot] column 
		pivot_rows = []
		for i in range(pivot, no_rows):
			if input_mat_gene[i][pivot] == 1:
				pivot_rows.append(i)
						
		if len(pivot_rows) == 0: 	#fail to find pivot, decoding fails.
			print ("Decompose fail, unable to find pivot for col %s" %pivot) 
			break
			
		#putting the first pivot rows to the top
		if pivot_rows[0] != pivot :
			input_mat_gene = row_ops(input_mat_gene, pivot, pivot_rows[0], 'ex')
			input_mat_msg = row_ops(input_mat_msg, pivot, pivot_rows[0], 'ex')
			del pivot_rows[0]
		
		#clearing values in [pivot] column below the [pivot] row
		for i in pivot_rows:
			if pivot == (no_cols): 	break	# the triangle matrix has been formed, no point continuing
			
			input_mat_gene= row_ops(input_mat_gene, i, pivot, 'xor')
			input_mat_msg = row_ops(input_mat_msg, i, pivot, 'xor')
			del pivot_rows[i]
			
	if pivot == (no_cols):
		del	input_mat_gene[no_cols:no_rows]  #removing bottom part of matrix
		del input_mat_msg[no_cols:no_rows] 	#^^
	
	return input_mat_gene, input_mat_msg
	
#solve triangular matrix into identity matrix, and thus decode the message
def solve_triangular_matrix(in_mat_gene, in_mat_msg):
	
	no_rows = len(in_mat_gene)  #number of rows of mat
	no_cols = len(in_mat_gene[0]) #number of columns of mat, assuming data inserted is a rectangular matrix
	
	for i in range(no_rows):		
		
		if i == no_rows:break   #cant continue with last row
		
		for j in range( i+1, no_cols ):  
			if in_mat_gene[i][j] == 1:			#	j > i, pivot value wont be affected
				in_mat_gene = row_ops(in_mat_gene, in_mat_gene[i], in_mat_gene[j], 'xor')
				in_mat_msg = row_ops(in_mat_msg, in_mat_msg[i], in_mat_msg[j], 'xor')
				
	return in_mat_gene, in_mat_msg	

#main function
def main():
	msg_length = 5
	k = msg_length 
	msg_mat = rand_msg_generation(k)
	tx_list_gene=[]
	tx_list_msg =matrix(GF(2), k+30, 1,)

	for i in range(k+30):
		gene=rand_gene_generation(k)
		coded_msg= gene*msg_mat
		tx_list_gene.append(gene)
		tx_list_msg[i]=coded_msg
		tx_list_msg.transpose()
		
	#check method to use multi return function
	rx_list_gene,rx_list_msg = rand_selection_kplus10(k,tx_list_gene, tx_list_msg)

	tri_mat_gene,tri_mat_msg= triangle_mat_decompo(rx_list_gene, rx_list_msg)

	inden_mat_gene,decode_msg= solve_triangular_matrix(tri_mat_gene, tri_mat_msg)

	#check if decode_msg = ori_msg
	if decode_msg == msg_mat:
		print("decode success")
	else:
		print("decode fail")

main()