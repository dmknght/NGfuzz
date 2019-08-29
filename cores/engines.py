import cores, requests
from cores import events


def fuzz(url, params, headers, payload, point, method):
	params, headers = cores.addPayload(params, headers, payload, point)
	response = send(url, method, params, headers)
	
	analysis(response, method, payload, point)
	if response.status_code != 404:
		checkVuln(payload, response.text, method, len(response.text), point)
	return True


def send(url, method, payload, headers):
	if method == "POST":
		resp = requests.post(url, data = payload, headers = headers)
	else:
		resp = requests.get(url, params = payload, headers = headers)
	return resp


def analysis(response, nameMethod, payload, point):
	events.fuzz_info(response.status_code, nameMethod, len(response.text), point, payload)


def checkVuln(payload, response, nameMethod, szResp, point):
	import importlib
	from modules import ActiveScan

	modules = cores.load_modules(ActiveScan)

	try:
		for module in modules:
			module = importlib.import_module('modules.%s' % (module))
			module = module.Check()
			module.payload = payload
			module.signatures = module.signature()
			result = module.fuzz(payload, response, nameMethod, szResp, point)
			if result:
				from cores import events
				events.fuzz_vuln(result, nameMethod, len(response), point, payload)
	except Exception:
		pass
