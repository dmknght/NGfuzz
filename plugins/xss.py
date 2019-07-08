import re
from cores import events

class Check(object):
	def __init__(self):
		self.payload = self.gen_payload()

	def check(self, browser):
		response = str(browser.get_current_page())
		match = re.findall(re.escape(self.payload), response)
		if match:
			self.found(browser.get_url())

	def gen_payload(self):
		return ["<script>alert(1);</script>"]

	def found(self, url):
		events.vulnerable("Reflected XSS", url)