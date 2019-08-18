def defOptions():
	options = {
		"-p": "",  # parameters
		"-i": "",  # inject parameters
		"-m": "GET",  # Packets method
		"-w": "",  # wordlist path
		"-t": 16,  # threads
	}
	
	return options


def getOptions():
	import sys
	if len(sys.argv) == 1:
		pass  # No arguments. do something
		return False
	else:
		i = 0
		options = defOptions()
		url = ""
		# TODO help banner
		while i < len(sys.argv):
			if sys.argv[i] in options.keys():
				options[sys.argv[i]] = sys.argv[i + 1]
				i += 1
			else:
				url = sys.argv[i]
			i += 1
		return url, options
