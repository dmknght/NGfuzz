import threading


def run_threads(threads):
	# Run threads
	for thread in threads:
		thread.start()
	
	# Wait for threads completed
	for thread in threads:
		thread.join()


def createTask(url, params, headers, payloads, points, method, threads):
	"""
		Create threads
	"""
	
	from cores import engines
	
	workers = []
	for point in points:
		for payload in payloads:
			"== Run and delete all threads if touch number of threads"
			if len(workers) == threads:
				run_threads(workers)
				del workers[:]
			
			"== Craft threads =="
			worker = threading.Thread(
				target = engines.fuzz,
				args = (url, params, headers, payload, point, method)
			)
			worker.daemon = True
			workers.append(worker)
		
		"== Run all threads == "
		run_threads(workers)
		del workers[:]
	
	return True
