from cores import events


def main():
	from UI import cli
	
	url, options = cli.getOptions()
	import cores
	url = cores.checkURL(url)
	
	try:
		threads = int(options["-t"])
		if threads < 1:
			events.error("Threads must be > 1", "ARGS")
			return False
	except ValueError:
		events.error("Threads must be a number", "ARGS")
		return False
	
	try:
		if not options["-w"]:
			events.error("Must give payloads to run", "ARGS")
			return False
		payloads = open(options["-w"]).read().split("\n")
	except IOError:
		events.error("Error while reading payload path", "ARGS")
		return False
	
	if "*FUZZ" not in url:
		if not options["-i"]:
			events.error("Must give parameter to inject", "ARGS")
			return False
		else:
			points = options["-i"].split(",")
		if "?" in url:
			params, values = cores.getParams(url.split("?")[1])
		else:
			if not options["-p"]:
				events.error("No parameter", "ARGS")
				return False
			params, values = cores.getParams(options["-p"])
		
		headers = {}
		if options["-H"]:
			for pair in options["-H"].split("\n"):
				key, value = pair.split(":")
				headers.update({key: value[1:]})

		import requests
		if options["-m"] == "GET":
			method = requests.get
		elif options["-m"] == "POST":
			method = requests.post
		
		from cores import fuzzer
		fuzzer.createTask(url, params, values, payloads, points, method, headers, threads)
		return True
	else:
		pass
import time

runtime = time.time()
try:
	result = main()
except:
	result = False

if result:
	events.success("Elapsed %0.2f" % (time.time() - runtime), "COMPLETED")
else:
	events.error("Elapsed %0.2f" % (time.time() - runtime), "ERROR")