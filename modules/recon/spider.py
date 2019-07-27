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
					
					# Remove "/" in last character
					if link[-1] == "/":
						last_slash = True
						link = link[:-1]
					else:
						last_slash = False
					if link and "://" not in link:
						if link[:3] == "../":
							# Link with above level
							link = "/".join(spider_url.split("/")[:-2]) + link.replace("..", "")
							link = link + "/" if last_slash else link
						else:
							# Move `/foo/`, `foo/` and `./foo/` to 1 format
							if link[:2] == "./":
								link = link[2:]
							elif link[:1] == "/":
								link = link[1:]
							if len(link.split("/")) == 1:
								link = "/".join(spider_url.split("/")[:-1]) + "/" + link
								link = link + "/" if last_slash else link
							else:
								link = spider_url + link + "/" if last_slash else spider_url + link
						
						# If URL is good
						if link and scope in link and "javascript:__" not in link and "javascript:" not in link and "mailto:" not in link:
							# If url is not visited
							if link not in all_urls.keys():
								link = cores.check_url(link)
								resp = browser.open(link)
								if resp.status_code < 400:
									all_urls.update({link: params})
									
									# Check if current url redirect us to other url with parameter
									current_url = browser.get_url()
									# If link is redirected
									if current_url != link:
										all_urls.update(cores.get_params(current_url))
							
							# Else, update new parameters only
							else:  # Check and add params here
								if params.keys()[0] not in all_urls[link].keys()[0]:
									all_urls[link].update(params)
					else:
						if scope in link:
							resp = browser.open(link)
							if resp.status_code < 400:
								all_urls.update({link: params})
								# Check if current url redirect us to other url with parameter
								current_url = browser.get_url()
								# If link is redirected
								if current_url != link:
									all_urls.update(cores.get_params(current_url))
			
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