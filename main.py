import mechanicalsoup, re
from cores import events

def load_modules():
	import os
	import plugins as module_path

	pwd = module_path.__path__[0]

	for root, dirs, files in os.walk(pwd):
		files = filter(lambda x: not x.startswith("__") and x.endswith(".py"), files)

	return [x.replace(".py", "") for x in files]

def scan_get(url, module_name):
	params = ["id"]
	import importlib
	module = importlib.import_module('plugins.%s' %(module_name))
	module = module.Check()

	browser = mechanicalsoup.StatefulBrowser()
	for payload in module.gen_payload():
		for param in params: # TODO edit here for multiple params
			module.payload = payload
			payloads = {param: payload}
			browser.open(url, params = payloads)# + payload)

			if module.check(browser):
				break
	browser.close()

def check_url(url):
	if "://" in url:
		if not url.startswith(("http://", "https://")):
			events.error("Invalid URL protocol")
	else:
		url = "http://%s" %(url)
	if len(url.split("/")) <= 3:
		url = "%s/" %(url) if url[-1] != "/" else url

	return url

url = check_url("http://192.168.57.3/show.php?id=1")
from modules import footprinting
footprinting.start(url)
from cores import spider
print("\n")
events.success(url, info = "Spider")
branches = spider.spider(url)
# if "no--crawl":
# 	branches = [spider.get_params(url)]
events.sub_info("Found %s URL[s]" %(len(branches)), "Spider")

modules = load_modules()
print("\n")
events.info("Loaded %s modules: %s" %(len(modules), modules), info = "Active scan")

for branch in branches:
	for module in modules:
		scan_get(branch, module)
