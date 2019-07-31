def info(data, info = "INFO"):
	print("[+] [\033[37m%s\033[00m] %s" %(info, data))

def sub_info(data, info = "INFO"):
	print(" [\033[37m%s\033[00m] [\033[36m%s\033[00m]" %(info, data))

def success(data, info = "INFO"):
	print("[*] [\033[32m%s\033[00m] [\033[32m%s\033[00m]" %(info, data))

def error(data, info = "ERR"):
	print("[x] [\033[31m%s\033[00m] %s" %(info, data))

def vuln_crit(vuln, url, parameter, payload):
	print("[*] [\033[31m%s\033[00m] [\033[4m\033[40m%s\033[00m] [\033[4m\033[31m%s\033[00m: \033[4m\033[33;1m%s\033[00m]" %(vuln, url, parameter, payload))

def sub_vuln_low(vuln, info):
	print(" [\033[34m%s\033[00m] [\033[31m%s\033[00m]" %(vuln, info))

def sub_vuln_med(vuln, info):
	print(" [\033[33m%s\033[00m] [\033[31m%s\033[00m]" %(vuln, info))
	
def fuzz_info(http_code, method, size, param, payload):
	print("[+] [\033[34m%s\033[00m] [%s] [%s] [\033[4m\033[31m%s\033[00m: \033[4m\033[33;1m%s\033[00m]" %(http_code, method, size, param, payload))
	
def fuzz_vuln(http_code, method, size, param, payload):
	print("[+] [\033[31m%s\033[00m] [%s] [%s] [\033[4m\033[31m%s\033[00m: \033[4m\033[33;1m%s\033[00m]" %(http_code, method, size, param, payload))