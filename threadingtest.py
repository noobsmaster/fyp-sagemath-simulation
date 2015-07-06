import time
from multiprocessing import Process, Value, Lock, Pool
def add_fail(failc, lock):
	time.sleep(0.01)
	with lock : failc.value += 1
	
if __name__ == '__main__':
	failcount = Value('i', 0)
	lock = Lock()
	pool = Pool()
	
	pool.map_async(add_fail(failcount,lock), range(10) )
	
	pool.close()
	pool.join()

	print (failcount.value)
