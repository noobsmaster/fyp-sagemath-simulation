from bitstring import BitArray
import copy
import random
#read documentation for random lib
#read documentation for bit array lib

def random_gene_generation(msg_length):
	
	return 

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
	no_cols = len(input_mat_gene[0]) #number of columns of mat
	
	for pivot in range(no_cols):
		
		#note: possible improvement, instead scanning until bottom, scan until encounter a pivot
		# identify rows with pivot at [pivot] column 
		pivot_rows = []
			
		for i in range(pivot, no_rows):
						
			if input_mat_gene[i].column(pivot) != 0:
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