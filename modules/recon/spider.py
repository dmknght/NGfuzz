import cores

all_urls = {}

def spider(url, branch = True):
	# from modules.recon import check_robots
	global all_urls

	# all_urls = check_robots.check(url) # TODO edit here
	link = cores.get_params(url)
	link, params = link.keys()[0], link.values()[0]
	all_urls.update({link: params})

	if branch == False:
		scope = cores.check_url(cores.get_domain(url))
	else:
		if url[-1] == "/":
			scope = url
		else:
			# scope = cores.check_url("/".join(url.split("/")[2:-1]))
			# scope = scope + "/" if scope[-1] != "/" else scope
			scope = cores.check_url("/".join(url.split("/")[2:-1]))
	visited = []
	import mechanicalsoup
	try:
		browser = mechanicalsoup.StatefulBrowser()
		for spider_url in all_urls.keys():
			if spider_url not in visited:
				browser.open(spider_url)
				visited.append(spider_url)

				for link in browser.links():
					link = cores.get_params(link.attrs['href'])
					link, params = link.keys()[0], link.values()[0]
					if link and "://" not in link:
						if link[:2] == "./":
							link = scope + link[2:]
						elif link[0] == "/": # /index.php for example, remove / and combine with urls
							link = scope[:-1] + link
						else:
							link = scope + link
					if link and scope in link and "javascript:__" not in link and "javascript:" not in link:
						if link not in all_urls.keys():
							link = cores.check_url(link) # TODO bug here
							all_urls.update({link: params})
						else: # Check and add params here
							if params.keys()[0] not in all_urls[link].keys()[0]:
								all_urls[link].update(params)

	except Exception as error:
		from cores import events
		events.error(error, "Spider")
	finally:
		try:
			browser.close()
		except:
			pass
		return all_urls
