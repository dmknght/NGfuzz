import cores, requests
from cores import events


def fuzz(url, params, headers, payload, point, method, first_page):
	params, headers = cores.addPayload(params, headers, payload, point)
	response = send(url, method, params, headers)
	
	analysis(response, method, payload, point, first_page)
	if response.status_code != 404:
		checkVuln(payload, response.text, method, len(response.text), point)
	return True


def send(url, method, payload, headers):
	if method == "POST":
		resp = requests.post(url, data = payload, headers = headers)
	else:
		resp = requests.get(url, params = payload, headers = headers)
	return resp


def analysis(response, name, payload, point, first_page):
	if response.status_code < 400:
		events.fuzz_info(response.status_code, name, len(response.text), point, payload)
	else:
		events.fuzz_info(response.status_code, response.title, len(response.text), point, payload)
	for line in cores.getdiff(first_page, response.text):
		events.diff_page(line)


def checkVuln(payload, response, name, szResp, point):
	import importlib
	from modules import ActiveScan

	modules = cores.load_modules(ActiveScan)

	try:
		for module in modules:
			module = importlib.import_module('modules.%s' % (module))
			module = module.Check()
			module.payload = payload
			module.signatures = module.signature()
			result = module.fuzz(payload, response, name, szResp, point)
			if result:
				from cores import events
				events.fuzz_vuln(result, name, len(response), point, payload)
	except Exception:
		pass
