import mechanicalsoup
from cores import events

def check(url):
	try:
		browser = mechanicalsoup.StatefulBrowser()

		pathlist, valid = [], []
		for line in str(browser.open("%srobots.txt" %(url) if "robots.txt" not in url else url).text).split("\n"):
			lineStr = str(line)
			path = lineStr.split(': /')
			if "Disallow" == path[0]:
					pathlist.append(path[1].replace("\n", "").replace("\r", ""))
					pathlist = list(set(pathlist))
			try:
					inx = pathlist.index("/")
					del pathlist[inx]
			except:
					pass
		if pathlist:
			events.info("%srobots.txt" %(url) if "robots.txt" not in url else url, info = "Robots")
			url = url.replace("robots.txt", "") if "robots.txt" in url else url

			for p in pathlist:
				disurl = url + p
				resp = browser.open(disurl)
				if resp.status_code == 200 or resp.status_code < 400:
					events.sub_info(disurl, info = "Found")
					valid.append(disurl)
	except:
		pass
	finally:
		browser.close()
		return valid
