import re
from cores import events

class Scanner(object):
	def __init__(self):
		self.payload = self.gen_payload()
		self.signatures = self.signature()

	def check(self, url, payload, response, parameter):
		for injection_types in self.signatures.keys():
			for sig in self.signatures[injection_types]:
				match = re.findall(re.escape(sig), response)
				if match:
					self.found(injection_types, url, parameter, payload)
					return True
		return False
	
	def fuzz(self, url, payload, response, parameter):
		for injection_types in self.signatures.keys():
			for sig in self.signatures[injection_types]:
				match = re.findall(re.escape(sig), response)
				if match:
					return self.signatures.keys()[0]
		return False

	def gen_payload(self):
		return []

	def signature(self):
		return {}

	def found(self, inject_type, url, parameter, payload):
		events.vuln_crit(inject_type, url, parameter, payload)