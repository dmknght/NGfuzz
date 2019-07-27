import cores

# TODO can't crawl all urls from root level
def spider(url, branch = True):
	# from modules.recon import check_robots
	all_urls = {}


	# all_urls = check_robots.check(url) # TODO edit here
	# link = cores.get_params(url).keys()[0]
	# link, params = link.keys()[0], link.values()[0]

	if branch == False:
		scope = cores.check_url(cores.get_domain(url))
	else:
		if url[-1] == "/":
			scope = url
		else:
			scope = cores.check_url("/".join(url.split("/")[2:-1]))
	all_urls.update({cores.get_params(scope).keys()[0]: cores.get_params(scope).values()[0]})
	visited = []
	import mechanicalsoup
	try:
		# TODO Invalid url protocol or DOM url
		browser = mechanicalsoup.StatefulBrowser()
		i = 0
		while all_urls.keys() != visited:
			try:
				spider_url = all_urls.keys()[i]
			except IndexError as error:
				break
			browser.open(spider_url)
			visited.append(spider_url)
			current_url = browser.get_url()
			if current_url != spider_url:
				all_urls.update({cores.get_params(current_url).keys()[0]: cores.get_params(current_url).values()[0]})
				
			# Start get all link in current page
			for _url in list(browser.links()):
				if "://" in _url.attrs['href'] and scope not in _url.attrs['href']:
					# If url is an other website, skip it
					pass
				else:
					# TODO BUG can't get url in branches
					# TODO work with scope range (branch and root)
					if "javascript:__" not in _url.attrs['href'] and "javascript:" not in _url.attrs['href'] and "mailto:" not in _url.attrs['href']:
						# DON'T WORK WITH JAVASCRIPT URL or mail url
						browser.follow_link(_url)
						current_url = browser.get_url()
						# If url is new -> add to url
						link = cores.get_params(current_url)
						if link.keys()[0] not in visited:
							# TODO GET all link in not visited
							# Open url and do stuff
							all_urls.update(link)
							visited.append(link.keys()[0])
	
						# If url is the same, check if it has different parameters
						else:
							# TODO check if parameter is different
							# Update parameters
							all_urls[link.keys()[0]].update(link.values()[0])
							visited.append(link.keys()[0])
			i += 1
	except AttributeError:
		pass
	except Exception as error:
		from cores import events
		events.error(error, "Spider")
	finally:
		from cores import events
		events.sub_info("Completed", "Spider")
		try:
			browser.close()
		except:
			pass
		return all_urls
