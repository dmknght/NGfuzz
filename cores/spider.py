from cores.actions import check_url, get_domain

def get_params(url):
	# TODO improve
	payloads = None
	try:
		url, payloads = url.split("?")

	except:
		pass
	finally:
		return [url, [payloads]]

all_urls, visited = [], []

def spider(url):
	global all_urls
	global visited

	scope = get_domain(url)

	import mechanicalsoup
	try:
		browser = mechanicalsoup.StatefulBrowser()
		browser.open(url)

		
		visited.append(url)
		for link in browser.links():
			_link = link.attrs['href']
			if "://" not in _link:
				if _link[0] == "/":
					_link = check_url(scope)[:-1] + _link
				else:
					_link = check_url(scope) + _link

			_url = get_params(_link)[0]
			if _url not in all_urls:
				response = browser.follow_link(link)
				if response.status_code < 400:
					all_urls.append(_url)
			for _url in all_urls:
				if _url not in visited:
					spider(_url)


	except Exception as error:
		from cores import events
		events.error(error)
	finally:
		try:
			browser.close()
		except:
			pass
		return all_urls
