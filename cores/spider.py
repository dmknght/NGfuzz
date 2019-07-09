from cores.actions import check_url, get_domain

# def get_params(url):
# 	# TODO improve
# 	param = ""
# 	try:
# 		url, payloads = url.split("?")
# 		for _ in payloads.split("&"):
# 			param, __ = _.split("=")

# 	except:
# 		pass
# 	finally:
# 		return [url, [param]]

all_urls = []

def spider(url):
	from modules import check_robots
	global all_urls

	all_urls = check_robots.check(url)

	scope = get_domain(url)

	import mechanicalsoup
	try:
		browser = mechanicalsoup.StatefulBrowser()
		browser.open(url)

		all_urls.append(url)

		for link in browser.links():
			_link = link.attrs['href']
			if "://" not in _link:
				if _link[0] == "/":
					_link = check_url(scope)[:-1] + _link
				else:
					_link = check_url(scope) + _link
			if _link not in all_urls:
				all_urls.append(_link)


	except Exception as error:
		from cores import events
		events.error(error)
	finally:
		try:
			browser.close()
		except:
			pass
		return all_urls
