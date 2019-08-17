import requests

from cores import makePayload

def sendGet(url, params, values, payload, point):
	# There is no injection point here
	# Have to think about it
	# No header fuzz TODO
	payload = makePayload(params, values, payload, point)
	response = requests.get(url, params = payload)
	return response

def sendPost(url, params, values, payload, point):
	# Still no fuzz point here
	# No header fuzz
	payload = makePayload(params, values, payload, point)
	response = requests.post(url, params = payload)
	return response