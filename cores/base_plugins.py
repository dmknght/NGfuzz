import re

class Check(object):
	def __init__(self):
		self.payload = self.gen_payload()
		self.sig = None

	def check(self, browser, payload):
		response = str(browser.get_current_page())
		for injection_types in self.sig.keys():
			for sig in self.sig[injection_types]:
				match = re.findall(re.escape(sig), response)
				if match:
					self.found(injection_types, browser.get_url())
					return True

	def gen_payload(self):
		return []

	def found(self, inject_type, url):
		events.vuln_crit(inject_type, url)
