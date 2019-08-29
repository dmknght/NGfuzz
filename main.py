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
		# Check for position
		if not options["-i"]:
			events.error("Must give parameter to inject", "ARGS")
			return False
		else:
			points = options["-i"].split(",")
		
		# Get headers
		headers = cores.makeHeader(options["-H"])
		
		# Get parameters
		if options["-m"] == "GET":
			if "?" in url:
				params, values = cores.getParams(url.split("?")[1])
			else:
				if options["-p"]:
					params, values = cores.getParams(options["-p"])
				else:
					params, values = "", ""
		else:
			if options["-p"]:
				params, values = cores.getParams(options["-p"])
			else:
				params, values = "", ""
		
		params = cores.makeParams(params, values)
		
		# TODO check if users don't give enough params

		if options["-m"] == "GET":
			method = "GET"
		elif options["-m"] == "POST":
			method = "POST"
		elif options["-m"] == "POST-FORM":
			method = "POST"
			headers.update({"Content-Type": "application/x-www-form-urlencoded"})
			# TODO add submit value automatically?
		else:
			events.error("Method is not supported", "ARGS")
			return False
		
		from cores import fuzzer
		fuzzer.createTask(url, params, headers, payloads, points, method, threads)
		return True
	else:
		pass
import time

runtime = time.time()
try:
	result = main()
except Exception:
	result = False

if result:
	events.success("Elapsed %0.2f" % (time.time() - runtime), "COMPLETED")
else:
	events.error("Elapsed %0.2f" % (time.time() - runtime), "ERROR")