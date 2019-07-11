def get_method(path, module_name):
	for url in path.keys():
		params = path[url]
		# Remove empty keys and values
		# https://stackoverflow.com/a/21482035
		params = {k: v for k, v in params.items() if v}
		if params:
			import importlib, mechanicalsoup
			try:
				browser = mechanicalsoup.StatefulBrowser()

				module = importlib.import_module('plugins.%s' %(module_name))
				module = module.Check()
				for key in params.keys():
					for payload in module.payload:
						# TODO no values, payload only
						send_payload = {k: "%s%s" %(params[k], payload) if k == key else params[k] for k in params.keys()}
						# print(send_payload)
						resp = browser.open(url, params = send_payload)
						try:
							resp = str(resp.text)
						except UnicodeEncodeError:
							resp = str(resp.text.encode('utf-8'))
						except:
							resp = ""
						if module.check(url, send_payload[key], resp, key):
							break
			except Exception as error:
				from cores import events
				events.error(error, "Scan GET")
			finally:
				browser.close()