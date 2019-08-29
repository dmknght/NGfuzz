from cores.base_plugins import Scanner
import re

class Check(Scanner):
	def gen_payload(self):
		from cores.xeger import Xeger
		generate = Xeger()
		while True:
			_payload = generate.xeger("((\%3C)|<)((\%69)|i|(\%49))((\%6D)|m|(\%4D))((\%67)|g|(\%47))[^\n]+((\%3E)|>)")
			if any(x in _payload for x in "\"'><;/"):
				return _payload
	
	def fuzz(self, payload, response, method, size, parameter):
		for injection_types in self.signatures.keys():
			for sig in self.signatures[injection_types]:
				match = re.findall(re.escape(sig), response)
				if match and any(x in payload for x in "><"):
					return injection_types
		return False
	
	def signature(self):
		return {"XSS" : [self.payload]}
