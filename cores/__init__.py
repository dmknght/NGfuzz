def load_modules(module_path):
	import os

	pwd = module_path.__path__[0]

	for root, dirs, files in os.walk(pwd):
		files = filter(lambda x: not x.startswith("__") and x.endswith(".py"), files)

	root = root.split("modules/")[1]
	return ["%s.%s" %(root, x.replace(".py", "")) for x in files]

def check_url(url):
	if "://" in url:
		if not url.startswith(("http://", "https://")):
			events.error("Invalid URL protocol")
	else:
		url = "http://%s" %(url)
	if len(url.split("/")) <= 3 or ("." not in url.split("/")[-1] and "?" not in url.split("/")[-1]):
	# if "." not in url.split("/")[-1] and "?" not in url.split("/")[-1]:
	# if len(url.split("/")) <= 3:
		url = "%s/" %(url) if url[-1] != "/" else url
	return url

def get_params(url):
	param, value = "", ""
	try:
		url, payloads = url.split("?")
		params = {param: value for param, value in [_.split("=") for _ in payloads.split("&")]}
	except ValueError:
		params = {'': ''}
	except Exception as error:
		from cores import events
		events.error(error)
	finally:
		return {url: params}

def get_domain(url):
	return url.split("/")[2]