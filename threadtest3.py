from multiprocessing import Pool, Value, Lock

def init(args,lock):
	fail_counter = args
	lock = lock
	

def add_fail(a):
	#print ('1')
	lock = Lock()
	with lock : failcount.value += 1

if __name__ == '__main__':
	failcount = Value('i', 0)
	lock = Lock()
	pool = Pool(initializer = init, initargs = (failcount,lock ))
	
	
	pool.map(add_fail, range(10), chunksize =1 )
	
	pool.close()
	
	pool.join()
		
	print(failcount.value)