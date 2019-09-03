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

		# Get headers
		headers = cores.makeHeader(options["-H"])
		
		# Get parameters
		if options["-X"] == "GET":
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

		if not options["-i"]:
			points = params.keys()
		else:
			points = options["-i"].split(",")

		if not points:
			events.error("Must give parameter to inject", "ARGS")
			return False
		# TODO check if users don't give enough params

		if options["-X"] == "GET":
			method = "GET"
		elif options["-X"] == "POST":
			method = "POST"
		elif options["-X"] == "POST-FORM":
			method = "POST"
			headers.update({"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"})
			# TODO add submit value automatically?
		else:
			events.error("Method is not supported", "ARGS")
			return False
		
		# TODO check url before fuzz
		from cores.engines import send
		response = send(url, method, params, headers)
		if response.status_code == 404:
			events.error("URL error 404", "CHECK")
		
		
		from cores import fuzzer
		fuzzer.createTask(url, params, headers, payloads, points, method, response.text, threads)
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