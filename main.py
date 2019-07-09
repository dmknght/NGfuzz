import mechanicalsoup, re
from cores import events

def load_modules():
	import os
	import plugins as module_path

	pwd = module_path.__path__[0]

	for root, dirs, files in os.walk(pwd):
		files = filter(lambda x: not x.startswith("__") and x.endswith(".py"), files)

	return [x.replace(".py", "") for x in files]

def scan(url, module_name):
	import importlib
	module = importlib.import_module('plugins.%s' %(module_name))
	module = module.Check()

	browser = mechanicalsoup.StatefulBrowser()
	for payload in module.gen_payload():
		module.payload = payload
		browser.open(url)# + payload)
		browser.select_form(nr = 0)
		browser['searchFor'] = payload
		browser.submit_selected()
		module.check(browser)
	browser.close()

def check_url(url):
	if "://" in url:
		if not url.startswith(("http://", "https://")):
			events.error("Invalid URL protocol")
	else:
		url = "http://%s" %(url)
	url = "%s/" %(url) if url[-1] != "/" else url

	return url

url = check_url("http://192.168.57.3/")
from modules import footprinting
footprinting.start(url)
from cores.spider import spider
events.success(url, info = "Spider")
branches = spider(url)
events.sub_info("Found %s URL[s]" %(len(branches)), "Spider")

modules = load_modules()
events.info("Loaded %s modules: %s" %(len(modules), modules), info = "Active scan")

# for module in modules:
# 	scan(url, module)
