from cores import events

def start(url):
	import mechanicalsoup

	browser = mechanicalsoup.StatefulBrowser()
	response = browser.open(url)
	header_analysis(response.headers)
	
	if response.status_code > 500:
		events.error("Server error: %s" %(response.status_code))
	elif response.status_code == 404:
		events.error("Link not found: %s" %(response.status_code))
		return False
	elif response.status_code == 403:
		events.error("Forbidden: %s" %(response.status_code))
		return False

	if str(browser.get_url()) != url:
		events.info("%s" %(browser.get_url()), info = "MOVED")
	browser.close()

def header_analysis(header):
	events.success(header["Date"])
	events.sub_info(header["Server"], "Server")
	events.sub_info(header["X-Powered-By"], "X-Powered-By")


def banner_grab():
	pass