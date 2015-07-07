from bitstring import BitArray
import copy
import random
import multiprocessing

fcount = None
#read documentation for random lib
#read documentation for bit array lib

#random row generation, the generation is on demand, rather then generating whole matrix before hand
def rand_gene_generation(msg_length):	# 1row x k-column
	
	gene_row = BitArray( [ random.choice ( [1,0] ) for i in range(msg_length) ] )
	
	return gene_row
	

#generate 1 column of random sym for msg randomize purpose	
def rand_msg_generation(msg_length):
	
	msg_col = [ BitArray( [random.choice ( [1,0] )] ) for i in range(msg_length) ]
	
	return msg_col			# k-row x 1column 


#random selection of ten Tx data 
def rand_selection_kplus10(tx_list_gen, tx_list_msg):
	k = len(tx_list_gen[0])
	pool_index_list = list( range( len(tx_list_gen) ) )
	chosen_list = []
		
	for i in range(k+10):
		chosen_list.append( pool_index_list.pop( random.randrange( len(pool_index_list))))
		
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
def row_ops (in_matrix, source_i, des_i, mode): 
	
	if mode == 'ex': #exchange mode, swaps row (only 1 line, consider integration)
		
		in_matrix[source_i],in_matrix[des_i] = in_matrix[des_i],in_matrix[source_i]
		
		return in_matrix
		
	if mode == 'xor' :	#xor operation mode, des=des xor source (only 1 line, consider integration)
		in_matrix[des_i] = in_matrix[des_i]^in_matrix[source_i]
		
		return in_matrix

#reducing matrix to triangular form, separate list for generator and message
def triangle_mat_decompo(input_mat_gene, input_mat_msg):
	
	no_rows = len(input_mat_gene)  #number of rows of mat
	no_cols = len(input_mat_gene[0]) #number of columns of mat
	
	for pivot in range(no_cols):
		
		#note: possible improvement, instead scanning until bottom, scan until encounter a pivot
		# identify rows with pivot at [pivot] column 
		pivot_rows = []
			
		for i in range(pivot, no_rows):
						
			if input_mat_gene[i][pivot] != 0:
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
	no_cols = len(in_mat_gene[0]) #number of columns of mat
	
	for i in range(no_rows):		
		
		if i == no_rows:
			break   #cant continue with last row
		
		for j in range( i+1, no_cols ):
			
			if in_mat_gene[i][j] != 0:  #	j > i, pivot value wont be affected
				
				in_mat_gene = row_ops(in_mat_gene, j, i, 'xor')
				in_mat_msg = row_ops(in_mat_msg, j, i, 'xor')
				
	return in_mat_gene, in_mat_msg	

#multiplication of vector for encoding
def msg_encoding(gen_row, msg_list):
	k=len(msg_list)
	encoded_symbol = BitArray('0b0')
	for i in range(k):
		if msg_list[i][0] != 0 and gen_row[i] != 0:
			encoded_symbol = encoded_symbol^BitArray('0b1')
	
	return 	encoded_symbol

#main	
def main(k, debug_opt=0):
	
	msg_list = rand_msg_generation(k)
	tx_list_gene= []
	tx_list_msg = []
	
	for i in range(k+30):
		gene=rand_gene_generation(k)
		coded_sym = msg_encoding(gene, msg_list)
		tx_list_gene.append(gene)
		tx_list_msg.append(coded_sym)
		
	if debug_opt==1 : print("tx_gen\n %s" %(tx_list_gene))
	if debug_opt==1 : print("tx_msg\n %s" %(tx_list_msg))
		
	rx_list_gene,rx_list_msg = rand_selection_kplus10(tx_list_gene, tx_list_msg)
	
	if debug_opt==1 : print("rx_gen\n %s" %(rx_list_gene))
	if debug_opt==1 : print("rx_msg\n %s" %(rx_list_msg))
				
	tri_mat_gene,tri_mat_msg= triangle_mat_decompo(rx_list_gene, rx_list_msg)
	
	if debug_opt==1 : print("tri_gen\n %s" %(tri_mat_gene))
	if debug_opt==1 : print("tri_msg\n %s" %(tri_mat_msg))
		
	iden_mat_gene,decode_msg= solve_triangular_matrix(tri_mat_gene, tri_mat_msg)

	if debug_opt==1 : print("identi_gen\n %s" %(iden_mat_gene))
	if debug_opt==1 : print("decode_msg\n %s" %(decode_msg))
		
	if debug_opt==1 : print("ori\n %s" %(msg_list)) 
	
	#check if decode_msg = ori msg
	if decode_msg == msg_list:
		if debug_opt==1 : print("decode success")
		return 1
		
	else:
		if debug_opt==1 : print("decode fail")
		return 0

def run_seq(a):
	global fcount
	global lock
	result = main (k=5) 			#msg length = 5 symbol
	
	if result == False :
		with lock : fcount.value += 1
		
def init(args1,args2):
	global fcount
	global lock
	fcount = args1
	lock = args2
		
if __name__ == '__main__':
	fcount = multiprocessing.Value('i',0)
	sample_size = 100		#times of simulation run to obtain result
	
	#threadcount = 1				#number of concurrency thread
	threadcount = multiprocessing.cpu_count()				#auto set based on number of logical CPU
	print ("\nUsing %d parallel thread(s)," %(threadcount))
	print ("For test case for k=5 running for %d times :" %(sample_size))
	
	lock = multiprocessing.Lock()
	pool = multiprocessing.Pool(threadcount, initializer = init, initargs = (fcount, lock))
	pool.map_async( run_seq, range(sample_size))

	pool.close()
	pool.join()
	failure = int(fcount.value)
		
	percent_fail= 100*failure/sample_size
	percent_success = 100 - percent_fail
	print ("Failure percentage = %f" %(percent_fail))
	print ("Success percentage = %f" %percent_success)