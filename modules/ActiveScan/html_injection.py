from cores.base_plugins import Scanner

class Check(Scanner):
	def gen_payload(self):
		return ["<img src='x' onerror=alert(1)/>"]

	def signature(self):
		return {"HTML Injection" : self.payload}
