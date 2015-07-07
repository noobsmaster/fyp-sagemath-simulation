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
	
	r=pool.map_async(add_fail, range(50000) )
	print (r._number_left)
	while (True):
		if (r.ready()): break # Jump out of while loop
		remaining = r._number_left # How many of the map call haven't been done yet?
		#remaining =1
		print ("Waiting for %d tasks to complete..." % remaining)
		time.sleep(0.25)
	
	pool.close()
	pool.join()
		
	print (fcount.value)
