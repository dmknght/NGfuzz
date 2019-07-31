from cores.base_plugins import Scanner

class Check(Scanner):
	def gen_payload(self):
		from cores.xeger import Xeger
		generate = Xeger()
		while True:
			_payload = generate.xeger("((\%3C)|<)((\%69)|i|(\%49))((\%6D)|m|(\%4D))((\%67)|g|(\%47))[^\n]+((\%3E)|>)")
			if any(x in _payload for x in "\"'><;/"):
				return _payload

	def signature(self):
		return {"XSS" : self.payload}
