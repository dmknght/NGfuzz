import mechanicalsoup, re
from cores import events
import time

def load_modules():
	import os
	import plugins as module_path

	pwd = module_path.__path__[0]

	for root, dirs, files in os.walk(pwd):
		files = filter(lambda x: not x.startswith("__") and x.endswith(".py"), files)

	return [x.replace(".py", "") for x in files]

def scan_get(path, module_name):
	import importlib
	module = importlib.import_module('plugins.%s' %(module_name))
	module = module.Check()

	browser = mechanicalsoup.StatefulBrowser()

	for url in path.keys():
		params = path[url]
		# Remove empty keys and values
		# https://stackoverflow.com/a/21482035
		params = {k: v for k, v in params.items() if v}
		# print params
		if params:
			for payload in module.payload:
				params = {k: payload for k in params.keys()}
				# print(params)
				# module.payload = payload
				# payloads = {param: payload}
				# browser.open(url, params = payloads)# + payload)
				browser.open(url, params = params)
				if module.check(browser, payload):
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

runtime = time.time()
url = check_url("http://aseafood.vn/")
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

for module in modules:
	scan_get(branches, module)
runtime = time.time() - runtime
events.success(time.strftime("%Y-%m-%d %H:%M"), "Elapsed: %0.2f" %(runtime))