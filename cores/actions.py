
def check_url(url):
	# if "://" in url:
	# 	if not url.startswith(("http://", "https://")):
	# 		events.error("Invalid URL protocol")
	# else:
	if "://" not in url:
		url = "http://%s" %(url)
	url = "%s/" %(url) if url[-1] != "/" else url

	return url

def get_domain(url):
	return url.split("/")[2]
