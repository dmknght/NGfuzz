from cores import events, actions

def start(url):
	import mechanicalsoup

	events.info(url, info = "Checking")
	domain = actions.get_domain(url)

	import socket#, GeoIP
	ip_addr = socket.gethostbyname(domain)
	events.sub_info(ip_addr, info = "IP Address")
	# ip_info = GeoIP.GeoIP()
	# events.sub_info("%s" %(ip_info.country_name_by_name(ip_addr)), info = "Country")

	browser = mechanicalsoup.StatefulBrowser()
	response = browser.open(url)
	try:
		title = str(browser.get_current_page().title.text.replace("\n", ""))
	except UnicodeEncodeError:
		title = str(browser.get_current_page().title.text.encode('utf-8')).replace("\n", "")
	except:
		title = "No Title"
	events.info(title, info = "Title")
	
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
	header_standards = (
		("X-Frame-Options", "SAMEORIGIN"),
		("X-XSS-Protection", "1; mode=block"),
		("X-Content-Type-Options", "nosniff"),
		("Content-Type", "text/html; charset=utf-8")
	)

	def check_section(header, name, value):
		try:
			if header[name] == value:
				events.sub_info(header[name], name)
			else:
				events.sub_vuln_low("Insecure value", "%s %s" %(name, header[name]))
		except:
			events.sub_vuln_low(name, "Missing Header")

	for check_values in header_standards:
		name, value = check_values
		check_section(header, name, value)


def banner_grab():
	pass