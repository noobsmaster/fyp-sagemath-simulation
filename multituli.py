from bitstring import BitArray
import copy
import random

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

#generation of workload
def work_prep(k, work_size):
	worklist_gen = []
	worklist_msg = []

	print ("\nPreparing work load of %d cycle of simulation..."%(100))
	for i in range(work_size):
		msg_list = rand_msg_generation(k)
		tx_list_gene= []
		tx_list_msg = []

		for gen_i in range(k+10):
			gene=rand_gene_generation(k)
			coded_sym = msg_encoding(gene, msg_list)
			tx_list_gene.append(gene)
			tx_list_msg.append(coded_sym)

		worklist_gen.append(tx_list_gene)
		worklist_msg.append(tx_list_msg)

	return (worklist_gen, worklist_msg)

def FormPartialUpperTriangularMatrix(partialMatIn,partialMatIn_msg):

	partialMat = copy.copy(partialMatIn)
	partialMat_msg = copy.copy(partialMat_msg)

	resultMat = []
	resultMsg = []
	nullRow = []
	errList = []
	m = len(partialMat)

	for pivotIndex in range(m):
		#search for 1 in the 1st column, break on 1st encounter, cut row from partial mat to result mat.
		for rowIndex in range(len(partialMat)):
			if partialMat[rowIndex][pivotIndex] != 0:
				resultMat.append(partialMat.pop([rowIndex]))
				resultMsg.append(partialMat_msg.pop([rowIndex]))
				break

		else :
			resultMat.append(nullRow)
			resultMsg.append(nullRow)
			errList.append(pivotIndex)
			continue
		#if not pivot not found, set row to null, add rowIndex into errList, continue for loop

		for rowIndex in range(len(partialMat)-1):
			if partialMat[rowIndex][pivotIndex] != 0:
				partialMat[rowIndex] = partialMat[rowIndex]^resultMat[pivotIndex]
				partialMat_msg[rowIndex] = partialMat_msg[rowIndex]^resultMsg[pivotIndex]

		#perform row opeartion to clear out column
		#rinse and repeat!

	if errList != []: #if errList not empty
		for rowIndex in err:
			resultMat[rowIndex] = partialMat.pop()
			resultMsg[rowIndex] = partialMat_msg.pop()
		#replace row in errList with leftover row in partial mat

	return resultMat,resultMsg

#forming upper triangular matrix as if 2 matrix are together, functions assuming len(top) >= len(btm)
def MergingPartialUpperTriangularMatrix(partialMatTop, partialMatBtm, partialMatTop_m, partialMatBtm_m):

	for columnIndex in range(len(partialMatTop)):
		if partialMatTop[columnIndex][columnIndex]==0:
			assert partialMatBtm[columnIndex][columnIndex] != 0 , "Unable to find pivot for row/column %d" % columnIndex #assert pivot can be found at btm if missin in top

			tempRow = copy.copy(partialMatTop[columnIndex]) 		#swap row from btm to top
			partialMatTop[columnIndex] = copy.copy(partialMatBtm[columnIndex])
			partialMatBtm[columnIndex] = copy.copy(tempRow)

			tempRow = copy.copy(partialMatTop_m[columnIndex]) 		#swap row from btm to top
			partialMatTop_m[columnIndex] = copy.copy(partialMatBtm_m[columnIndex])
			partialMatBtm_m[columnIndex] = copy.copy(tempRow)

		#clear bottom left quarter
		for rowIndex in range(len(partialMatBtm)):
			if partialMatBtm[rowIndex][columnIndex] != 0
				partialMatBtm[rowIndex] = partialMatBtm[rowIndex]^partialMatTop[columnIndex]
				partialMatBtm_m[rowIndex] = partialMatBtm_m[rowIndex]^partialMatTop_m[columnIndex]

	return partialMatTop, partialMatBtm, partialMatTop_m, partialMatBtm_m

#splitting matrix into more equal matrix , top must be >= btm
def splitting_mat(gene_mat, cmsg_column):
	
	gene_top = []
	gene_btm = []
	cmsg_top = []
	cmsg_btm = []
	
	input_len = len(gene_mat)
	if (input_len % 2 != 0):
		input_len = input_len - 1
	out_len_btm = input_len/2
	
	for rowIndex in range(out_len_btm):		#put number of rows in btm based on divided number
		gene_btm.append(gene_mat.pop())
		cmsg_btm.append(cmsg_column.pop())
	
	gene_top = gene_mat						#put rest of the rows in top
	cmsg_top = cmsg_column
	
	return gene_top, gene_btm, cmsg_top, cmsg_btm


def main():
	k = 6

	msg_column = rand_msg_generation(k)
	gene_mat = random_gene_generation(k)
	encoded_msg_column = []

	for i in range(len(gene_mat)):		#encoding msg to a column
		encoded_msg_column.append(msg_encoding(gene_mat[i],msg_column))

	remain_msg_len = len(msg_column)
	
	while remain_msg_len > 4:
		gene_top, gene_btm, cmsg_top, cmsg_btm = splitting_mat(gene_mat, encoded_msg_column)
		
		tri_gene_top, tri_msg_top = FormPartialUpperTriangularMatrix(gene_top, cmsg_top)
		tri_gene_btm, tri_msg_btm = FormPartialUpperTriangularMatrix(gene_btm, cmsg_btm)
		
		MergingPartialUpperTriangularMatrix(tri_gene_top, tri_gene_btm, tri_msg_top, tri_msg_btm)
