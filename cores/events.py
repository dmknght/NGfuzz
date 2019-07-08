def info(data, info = "INFO"):
	print("\n[+] [\033[37m%s\033[00m] %s" %(info, data))

def sub_info(data, info = "INFO"):
	print(" [\033[37m%s\033[00m] [\033[36m%s\033[00m]" %(info, data))

def success(data, info = "INFO"):
	print("\n[*] [\033[32m%s\033[00m] [\033[32m%s\033[00m]" %(info, data))

def error(data, info = "ERR"):
	print("\n[x] [\033[31m%s\033[00m] %s" %(info, data))

def vuln_crit(vuln, url):
	print("\n[*] [\033[31m%s\033[00m] [\033[4m\033[40m%s\033[00m]" %(vuln, url))

def sub_vuln_low(vuln, info):
	print(" [\033[34m%s\033[00m] [\033[31m%s\033[00m]" %(vuln, info))