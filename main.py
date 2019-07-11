import cores
from cores import events
import time

runtime = time.time()
url = cores.check_url("http://testphp.vulnweb.com/")
from modules import footprinting
footprinting.start(url)
from modules import spider
print("\n")
events.success(url, info = "Spider")
branches = spider.spider(url)
# if "no--crawl":
# 	branches = [cores.get_params(url)]
events.sub_info("Found %s URL[s]" %(len(branches)), "Spider")

modules = cores.load_modules()
print("\n")
events.info("Loaded %s modules: %s" %(len(modules), modules), info = "Active scan")
from cores import scan
for module in modules:
	scan.get_method(branches, module)
runtime = time.time() - runtime
events.success(time.strftime("%Y-%m-%d %H:%M"), "Elapsed: %0.2f" %(runtime))