import re

class Scanner(object):
	def __init__(self):
		self.payload = self.gen_payload()
		self.signature = self.signature()

	def check(self, browser, payload):
		response = str(browser.get_current_page())
		for injection_types in self.signature.keys():
			for sig in self.signature[injection_types]:
				match = re.findall(re.escape(sig), response)
				if match:
					self.found(injection_types, browser.get_url())
					return True

	def gen_payload(self):
		return []

	def signature(self):
		return {}

	def found(self, inject_type, url):
		events.vuln_crit(inject_type, url)
