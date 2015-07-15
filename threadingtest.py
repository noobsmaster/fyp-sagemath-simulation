from bitstring import BitArray
import copy
import random
import multiprocessing
import time

def rand_gene_generation(msg_length):	# 1row x k-column
	
	gene_row = BitArray( [ random.choice ( [1,0] ) for i in range(msg_length) ] )
	
	return gene_row
	

#generate 1 column of random sym for msg randomize purpose	
def rand_msg_generation(msg_length):
	
	msg_col = [ BitArray( [random.choice ( [1,0] )] ) for i in range(msg_length) ]
	
	return msg_col			# k-row x 1column 


#multiplication of vector for encoding
def msg_encoding(gen_row, msg_list):
	k=len(msg_list)
	encoded_symbol = BitArray('0b0')
	for i in range(k):
		if msg_list[i][0] != 0 and gen_row[i] != 0:
			encoded_symbol = encoded_symbol^BitArray('0b1')
	
	return 	encoded_symbol
	
k=5
sample_size=100

worklist_gen = []
worklist_msg = []
for i in range(sample_size):
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
		
to_file_1 = open('file1','w+b')
to_file_2 = open('file2','w+b')

to_file_1.write(worklist_gen)
to_file_2.write(worklist_msg)

gen = to_file_1.read()
msg = to_file_2.read()

if gen == worklist_gen :
	print ('yes')