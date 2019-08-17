import threading


def run_threads(threads):
	# TODO progress bar
	# Run threads
	for thread in threads:
		thread.start()
	
	# Wait for threads completed
	for thread in threads:
		thread.join()


def createTask(url, params, values, payloads, points, method, headers, threads):
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
				args = (url, params, values, payload, headers, point, method)
			)
			worker.daemon = True
			workers.append(worker)
		
		"== Run all threads == "
		run_threads(workers)
		del workers[:]
	
	return True
