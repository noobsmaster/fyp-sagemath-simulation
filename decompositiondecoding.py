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
		
	else if mode == 'xor' #xor operation mode, des=des xor source
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
		if pivot_rows[0] != pivot
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
		
def solve_triangular_matrix(in_mat_gene, in_mat_msg):
	
	no_rows = len(in_mat_gene)  #number of rows of mat
	no_cols = len(in_mat_gene[0]) #number of columns of mat, assuming data inserted is a rectangular matrix
	
	for i in range(no_rows):		
		
		if i = no_rows:break   #cant continue with last row
		
		for j in range( i+1, no_cols ):  
			if in_mat_gene[i][j] == 1:			#	j > i, pivot value wont be affected
				in_mat_gene = row_ops(in_mat_gene, in_mat_gene[i], in_mat_gene[j], 'xor')
				in_mat_msg = row_ops(in_mat_msg, in_mat_msg[i], in_mat_msg[j], 'xor')
				
	return in_mat_gene, in_mat_msg	



















				