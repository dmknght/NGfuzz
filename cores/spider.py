from cores.actions import check_url, get_domain

def get_params(url):
	# TODO test with multiple arguments
	param, value = "", ""
	try:
		url, payloads = url.split("?")
		param, value = [_.split("=") for _ in payloads.split("&")][0]

	except ValueError:
		pass
	except Exception as error:
		from cores import events
		events.error(error)
	finally:
		return {url: {param: value}}

# recursion
# def spider(url):
# 	from modules import check_robots
# 	# global all_urls
# 	all_urls = []

# 	all_urls = check_robots.check(url)

# 	# scope = get_domain(url)
# 	def crawl(url, all_links):
# 		if url in all_links:
# 			return all_links
# 		try:
# 			import mechanicalsoup
# 			browser = mechanicalsoup.StatefulBrowser()
# 			browser.open(url)
# 			scope = get_domain(url)
# 			for link in browser.links():
# 				_link = check_url(scope) + link.attrs['href']
# 				if _link not in all_links and scope in _link:
# 					all_links.append(_link)
# 			for _url in all_links:
# 				all_links = crawl(_url, all_links)
# 		except Exception as error:
# 			events.error(error)
# 		finally:
# 			return all_links
# 	return crawl(url, all_urls)


all_urls = {}

def spider(url):
	from modules import check_robots
	global all_urls

	# all_urls = check_robots.check(url)
	link = get_params(url)
	link, params = link.keys()[0], link.values()[0]
	all_urls.update({link: params})

	scope = get_domain(url)

	import mechanicalsoup
	try:
		import traceback
		browser = mechanicalsoup.StatefulBrowser()
		browser.open(url)


		for link in browser.links():
			link = get_params(link.attrs['href'])
			link, params = link.keys()[0], link.values()[0]
			if "://" not in link:
				if link[0] == "/": # /index.php for example, remove / and combine with urls
					link = check_url(scope)[:-1] + link
				else:
					link = check_url(scope) +link
			if scope in link and "javascript:__" not in link:
				if link not in all_urls.keys(): # TODO subdomain
					# all_urls.append({link: params})
					all_urls.update({link: params})
				else: # Check and add params here
					if params.keys()[0] not in all_urls[link].keys()[0]:
						all_urls[link].update(params) # TODO test with multiple params

	except Exception as error:
		traceback.print_exc()
		from cores import events
		events.error(error)
	finally:
		try:
			browser.close()
		except:
			pass
		return all_urls
