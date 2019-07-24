import cores
from cores import events
import time

runtime = time.time()
url = cores.check_url("http://192.168.56.103/owaspbricks/")
from modules.recon import footprinting
footprinting.start(url)
# if option spider
from modules.recon import spider
print("\n")
branch = True
events.success(url, "Spider")
branches = spider.spider(url, branch = branch)
print(branches)
# if "no--crawl":
# 	branches = [cores.get_params(url)]
events.sub_info("Found %s URL[s]" %(len(branches)), info = "Root" if not branch else "Branch")

from modules import ActiveScan
# print(branches)
modules = cores.load_modules(ActiveScan)
print("\n")
events.info("Loaded %s modules: %s" %(len(modules), modules), info = "Scanner")
from cores import scan
for module in modules:
	try:
		scan.get_method(branches, module)
	except KeyboardInterrupt:
		events.error("Interrupted by user", "SCAN")
		break
runtime = time.time() - runtime
events.success(time.strftime("%Y-%m-%d %H:%M"), "Elapsed: %0.2f" %(runtime))