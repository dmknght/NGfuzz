from cores.base_plugins import Scanner

class Check(Scanner):
	def gen_payload(self):
		return ["<script>alert(1);</script>"]

	def signature(self):
		return {"XSS" : self.payload}
