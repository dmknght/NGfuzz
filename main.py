import mechanicalsoup, re
from cores import events

def load_modules():
	import os
	import plugins as module_path
	pwd = module_path.__path__[0]
	for root, dirs, files in os.walk(pwd):
		files = filter(lambda x: not x.startswith("__") and x.endswith(".py"), files)
	# return files
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

modules = load_modules()
events.info("Loaded %s modules: %s" %(len(modules), modules))
# print("Loaded %s modules" %(len(modules)))
# print(modules)
for module in modules:
	scan("http://testphp.vulnweb.com/", module)
	# scan("http://testphp.vulnweb.com/listproducts.php?cat=1", module)
