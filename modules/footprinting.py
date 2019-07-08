from cores import events

def start(url):
	import mechanicalsoup

	browser = mechanicalsoup.StatefulBrowser()
	response = browser.open(url)

	events.info(str(browser.get_current_page().title.text.replace("\n", "")), "Home")
	
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
	header_info(response.headers)
	header_analysis(response.headers)

	import check_robots
	check_robots.check(url)

	browser.close()

def header_info(header):
	# print(header)
	events.success(header["Date"], info = "Header")
	try:
		events.sub_info(header["Server"], "Server")
		events.sub_info(header["X-Powered-By"], "X-Powered-By")
		if header["X-Powered-By"] == "ASP.NET":
			events.sub_info(header["X-AspNet-Version"], "X-AspNet-Version")
	except:
		pass

def header_analysis(header):
	try:
		header["X-XSS-Protection"]
	except:
		events.sub_vuln_low("Header Missing", "X-XSS-Protection")


def banner_grab():
	pass