from cores.actions import check_url, get_domain
from cores import events

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

# all_urls = []

def spider(url):
	from modules import check_robots
	# global all_urls
	all_urls = []

	all_urls = check_robots.check(url)

	# scope = get_domain(url)
	def crawl(url, all_links):
		if url in all_links:
			return all_links
		try:
			import mechanicalsoup
			browser = mechanicalsoup.StatefulBrowser()
			browser.open(url)
			scope = get_domain(url)
			for link in browser.links():
				_link = check_url(scope) + link.attrs['href']
				if _link not in all_links and scope in _link:
					all_links.append(_link)
			for _url in all_links:
				all_links = crawl(_url, all_links)
		except Exception as error:
			events.error(error)
		finally:
			return all_links
	return crawl(url, all_urls)

