def info(data):
	print("[+] [\033[32mINFO\033[00m] %s" %(data))

def vulnerable(vuln, url):
	print("[*] [\033[31m%s\033[00m] [\033[4m\033[40m%s\033[00m]" %(vuln, url))