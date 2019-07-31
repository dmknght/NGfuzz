"""
submit():
	response = submit(url, payload)
	for modules in import_module:
		modules.check(response, payload)

for payload in payloads
	threading.run(submit(payload, options))

"""


def get_method(url, params, fuzz_params, payloads, threads = 16):
	def run_threads(threads):
		# TODO progress bar
		# Run threads
		for thread in threads:
			thread.start()
		
		# Wait for threads completed
		for thread in threads:
			thread.join()
	
	def send_inject(url, fuzz_param = "None", payload, inject_point = "*FUZZ*"):
		# TODO parse fuzz_param
		try:
			import mechanicalsoup
			# TODO add proxy
			browser = mechanicalsoup.StatefulBrowser()
			response = browser.open(url.replace(inject_point, payload)) # TODO url encode
		except Exception as error:
			from cores import events
			events.error(error, "FUZZ")
		finally:
			browser.close()
		
		try:
			resp = str(response.text)
		except UnicodeEncodeError:
			resp = str(response.text.encode('utf-8'))
		except Exception:
			resp = ""
		
		# TODO check HTTP code
		import importlib, cores
		from modules import ActiveScan
		modules = cores.load_modules(ActiveScan)
		for module in modules:
			module = importlib.import_module('modules.%s' % (module))
			module = module.Check()
			
			# Re-generate payload and signature. Work for XSS
			module.payload = payload
			module.signatures = module.signature()
			
			result = module.fuzz(url, payload, resp, fuzz_param)
		# If not found any vuln, print something
		if not result:
			if response.status_code != 403:
				from cores import events
				events.fuzz_info(response.status_code, "GET", len(resp), fuzz_param, payload)
		else:
			from cores import events
			events.fuzz_vuln(result, "GET", len(resp), fuzz_param, payload)
	
	def send_param(url, params, fuzz_param, payload):
		try:
			import mechanicalsoup
			# TODO add proxy
			browser = mechanicalsoup.StatefulBrowser()
			send_payload = {k: "%s" % (payload) if k == fuzz_param else params[k] for k in params.keys()}
			response = browser.open(url, params = send_payload)
		except Exception as error:
			from cores import events
			events.error(error, "FUZZ")
		finally:
			browser.close()
		
		try:
			resp = str(response.text)
		except UnicodeEncodeError:
			resp = str(response.text.encode('utf-8'))
		except Exception:
			resp = ""
		
		# TODO check HTTP code
		import importlib, cores
		from modules import ActiveScan
		modules = cores.load_modules(ActiveScan)
		for module in modules:
			module = importlib.import_module('modules.%s' % (module))
			module = module.Check()
			
			# Re-generate payload and signature. Work for XSS
			module.payload = payload
			module.signatures = module.signature()

			result = module.fuzz(url, payload, resp, fuzz_param)
		# If not found any vuln, print something
		if not result:
			if response.status_code != 403:
				from cores import events
				events.fuzz_info(response.status_code, "GET", len(resp), fuzz_param, payload)
		else:
			from cores import events
			events.fuzz_vuln(result, "GET", len(resp), fuzz_param, payload)
		
		
	try:
		params = {k: v for k, v in params.items() if v}  # TODO check here
		workers = []
		import threading
		for fuzz_param in fuzz_params:
			for payload in payloads:
				# Fill thread pool, run them all
				if len(workers) == threads:
					run_threads(workers)
					del workers[:]
				worker = threading.Thread(
					target = send_param,
					args = (url, params, fuzz_param, payload)
				)
				worker.daemon = True
				workers.append(worker)
		
		# Run all last threads
		run_threads(workers)
		del workers[:]
						
	except Exception as error:
		from cores import events
		events.error(error, "Fuzz GET")