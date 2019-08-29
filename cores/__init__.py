def load_modules(module_path):
	import os
	pwd = module_path.__path__[0]

	for root, dirs, files in os.walk(pwd):
		files = filter(lambda x: not x.startswith("__") and x.endswith(".py"), files)
	
	root = root.split("modules/")[1]
	return ["%s.%s" % (root, x.replace(".py", "")) for x in files]


def checkURL(url):
	if "://" in url:
		if not url.startswith(("http://", "https://")):
			events.error("Invalid URL protocol")
	else:
		url = "http://%s" % (url)
	if len(url.split("/")) <= 3 or ("." not in url.split("/")[-1] and "?" not in url.split("/")[-1]):
		# if "." not in url.split("/")[-1] and "?" not in url.split("/")[-1]:
		# if len(url.split("/")) <= 3:
		url = "%s/" % (url) if url[-1] != "/" else url
	return url


# def get_params(url):
# 	param, value = "", ""
# 	split_char = ""
# 	# TODO handle DOM object for DOM XSS
# 	try:
# 		# GET PARAMETERS FROM URL
# 		# ? FOR GET PARAMS, # FOR DOM
# 		if "?" in url:
# 			split_char = "?"
# 		elif "#" in url:
# 			split_char = "#"
# 		url, payloads = url.split(split_char)
# 		params = {param: value for param, value in [_.split("=") for _ in payloads.split(split_char)]}
# 	except ValueError:
# 		params = {'': ''}
# 	except Exception as error:
# 		from cores import events
# 		events.error(error)
# 	finally:
# 		return {url: params}

def getParams(payload):
	params, values = [], []
	# payload = url.split("?")[1]
	for pair in payload.split("&"):
		param, value = pair.split("=")
		params.append(param)
		values.append(value)
	return params, values

def getDomain(url):
	return url.split("/")[2]


def makeHeader(header):
	retHeader = {}
	if header:
		for pair in header.split("\n"):
			key, value = pair.split(":")
			retHeader.update({key: value[1:]})
		
	return retHeader
	
def makeParams(params, values):
	retParam = {}
	for param, value in zip(params, values):
		retParam.update({param: value})
	return retParam

def addPayload(params, headers, payload, point):
	if point in params.keys():
		params[point] = payload
	else:
		headers[point] = payload
		
	return params, headers