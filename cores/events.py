def info(data, info = "INFO"):
	print("[+] [\033[37m%s\033[00m] %s" %(info, data))

def sub_info(data, info = "INFO"):
	print(" [\033[37m%s\033[00m] [\033[36m%s\033[00m]" %(info, data))

def success(data, info = "INFO"):
	print("[*] [\033[32m%s\033[00m] [\033[32m%s\033[00m]" %(info, data))

def error(data, info = "ERR"):
	print("[x] [\033[31m%s\033[00m] %s" %(info, data))

def vulnerable(vuln, url):
	print("[*] [\033[31m%s\033[00m] [\033[4m\033[40m%s\033[00m]" %(vuln, url))