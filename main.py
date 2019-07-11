import cores
from cores import events
import time

runtime = time.time()
url = cores.check_url("http://www.nutrivision.vn/?php=product_detail&id=295")
from modules.recon import footprinting
footprinting.start(url)
# if option spider
from modules.recon import spider
print("\n")
events.success(url, info = "Spider")
branches = spider.spider(url)
# if "no--crawl":
# 	branches = [cores.get_params(url)]
events.sub_info("Found %s URL[s]" %(len(branches)), "Spider")

from modules import ActiveScan
modules = cores.load_modules(ActiveScan)
print("\n")
events.info("Loaded %s modules: %s" %(len(modules), modules), info = "Active scan")
from cores import scan
for module in modules:
	scan.get_method(branches, module)
runtime = time.time() - runtime
events.success(time.strftime("%Y-%m-%d %H:%M"), "Elapsed: %0.2f" %(runtime))