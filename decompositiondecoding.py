
#row operation functions, xor and exchange
def row_ops (matrix, source_i, des_i, mode): 
	
	if mode == 'ex': #exchange mode, swaps row
		row_op_temp = []
		row_op_temp = matrix[source_i]
		matrix[des_i] = matrix[source_i]
		matrix[source_i] = row_op_temp
		
		return matrix
		
	else if mode == 'xor' #xor operation, des=des xor source
		matrix[des_i] = matrix[des_i].__xor__(input_mat[pivot])
		
		return matrix
	
def triangle_mat_decompo(input_mat):
		
	for pivot in range(len(input_mat[0])):	#pivot at [value] column
		
		# identify rows with pivot at [pivot] column
		pivot_rows = []
		for i in range(pivot, len(input_mat)):
			if input_mat[i][pivot] == 1:
				pivot_rows.append(i)
						
		#putting the first pivot rows to the top
		if pivot_rows[0] != pivot
			row_ops(input_mat, pivot, pivot_rows[0], 'ex')
			del pivot_rows[0]
		
		#clearing values in [pivot] column except pivot row
		for i in pivot_rows:
			row_ops(input_mat, i, pivot, 'xor')
			del pivot_rows[i]
		
	return input_mat	
		
def solve_triangular_matrix(input_mat):
	
	