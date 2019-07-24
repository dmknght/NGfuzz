import cores


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
		# TODO Invalid url protocol
		# TODO DOM URLs
		browser = mechanicalsoup.StatefulBrowser()
		i = 0
		while all_urls.keys() != visited:
			try:
				spider_url = all_urls.keys()[i]
			except IndexError:
				break
			if spider_url not in visited:
				browser.open(spider_url)
				visited.append(spider_url)
				current_url = browser.get_url()
				if current_url != spider_url:
					all_urls.update({cores.get_params(current_url).keys()[0]: cores.get_params(current_url).values()[0]})
					
				# Start get all link in current page
				for link in browser.links():
					link = cores.get_params(link.attrs['href'])
					link, params = link.keys()[0], link.values()[0]
					if link and "://" not in link:
						if link[:3] == "../":
							# Link with above level
							link = "/".join(spider_url.split("/")[:-2]) + link.replace("..", "")
						elif link[:2] == "./":
							# Link with current level but use ./
							link = spider_url + link[2:]
						elif link[0] == "/": # /index.php for example, remove / and combine with urls
							link = spider_url[:-1] + link
						else:
							# Remove "/" in last character
							link = link[:-1] if link[-1] == "/" else link
							if len(link.split("/")) == 1:
								# href contains url in same level
								link = "/".join(spider_url.split("/")[:-1]) + "/" + link
							else:
								# different level
								link = spider_url + link
								
					# If URL is good

					if link and scope in link and "javascript:__" not in link and "javascript:" not in link:
						# If url is not visited
						if link not in all_urls.keys():
							link = cores.check_url(link)
							all_urls.update({link: params})
							
							# Check if current url redirect us to other url with parameter
							try:
								browser.open(link)
								current_url = browser.get_url()
								# If link is redirected
								if current_url != link:
									all_urls.update(cores.get_params(current_url))
							except:
								pass
						# Else, update new parameters only
						else: # Check and add params here
							if params.keys()[0] not in all_urls[link].keys()[0]:
								all_urls[link].update(params)
			i += 1

	except Exception as error:
		from cores import events
		events.error(error, "Spider")
	finally:
		try:
			browser.close()
		except:
			pass
		return all_urls
