import cores
from cores import events


def fuzz(url, params, values, payload, headers, point, method):
	payload = cores.makePayload(params, values, payload, point)
	response = send(url, method, payload, headers)
	
	nameMethod = method.__name__.upper()
	analysis(response, nameMethod, payload, point)
	if response.status_code != 404:
		checkVuln(payload, response.text, nameMethod, len(response.text), point)
	# TODO fuzz headers
	return True


def send(url, method, payload, headers):
	resp = method(url, params = payload, headers = headers)
	return resp


def analysis(response, nameMethod, payload, point):
	events.fuzz_info(response.status_code, nameMethod, len(response.text), point, payload)


def checkVuln(payload, response, nameMethod, szResp, point):
	import importlib
	from modules import ActiveScan

	modules = cores.load_modules(ActiveScan)

	for module in modules:
		module = importlib.import_module('modules.%s' % (module))
		module = module.Check()
		module.payload = payload
		module.signatures = module.signature()
		result = module.fuzz(payload, response, nameMethod, szResp, point)
		if result:
			from cores import events
			events.fuzz_vuln(result, nameMethod, len(response), point, payload)
