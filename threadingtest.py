import time
from multiprocessing import Value, Lock, Pool
fcount = None

def add_fail(a):
	global fcount
	global lock
	with lock :
		fcount.value += 1
	return("1")	#problem with return

def print_1(a):
	print('##2')
	print (fcount.value)
	print(a)
	
	
	time.sleep(1)

def init(args1,args2):
	global fcount
	global lock
	fcount = args1
	lock = args2
	
if __name__ == '__main__':
	fcount = Value('i', 0)
	lock = Lock()
	pool = Pool(initializer = init, initargs = (fcount,lock ))
	a=1
	
	pool.map(add_fail, range(50000) )
	
	pool.close()
	pool.join()
		
	print (fcount.value)
