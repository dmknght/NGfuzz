from cores.base_plugins import Scanner

class Check(Scanner):
	def gen_payload(self):
		from cores.xeger import Xeger
		generate = Xeger()
		return [generate.xeger("((\%3C)|<)((\%2F)|\/)*[a-z0-9\%]+((\%3E)|>)")]

		# return ["<script>alert(1);</script>"]

	def signature(self):
		return {"XSS" : self.payload}
