from cores import makePayload


def fuzz(url, params, values, payload, headers, point, method):
	payload = makePayload(params, values, payload, point)
	response = send(url, method, payload, headers)
	
	
	# TODO analysis response here
	# TODO fuzz headers
	return True


def send(url, method, payload, headers):
	resp = method(url, params = payload, headers = headers)
	return resp
