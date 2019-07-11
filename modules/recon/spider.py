from cores.actions import check_url, get_domain
import cores

all_urls = {}

def spider(url):
	# from modules.recon import check_robots
	global all_urls

	# all_urls = check_robots.check(url) # TODO edit here
	link = cores.get_params(url)
	link, params = link.keys()[0], link.values()[0]
	all_urls.update({link: params})

	scope = get_domain(url)

	import mechanicalsoup
	try:
		browser = mechanicalsoup.StatefulBrowser()
		browser.open(url)


		for link in browser.links():
			link = cores.get_params(link.attrs['href'])
			link, params = link.keys()[0], link.values()[0]
			if "://" not in link:
				if link[:2] == "./":
					link = check_url(scope)[:-2] + link
				elif link[0] == "/": # /index.php for example, remove / and combine with urls
					link = check_url(scope)[:-1] + link
				else:
					link = check_url(scope) +link
			if scope in link and "javascript:__" not in link:
				if link not in all_urls.keys(): # TODO subdomain
					# all_urls.append({link: params})
					all_urls.update({link: params})
				else: # Check and add params here
					if params.keys()[0] not in all_urls[link].keys()[0]:
						all_urls[link].update(params)

	except Exception as error:
		from cores import events
		events.error(error)
	finally:
		try:
			browser.close()
		except:
			pass
		return all_urls
