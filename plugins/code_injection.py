from cores.base_plugins import Scanner

class Check(Scanner):
	def gen_payload(self):
		return [
			";env",
			"a;env",
			"a);env",
			"[VALUE];env",
			"[VALUE][LF]env",
			"/e\0",
			"a;exit(base64_decode('dzRwMXQxX2V2YWw='));//",
			# "a;exit(base64_decode('dzRwMXQxX2V2YWw='));#",
			# "\";exit(base64_decode('dzRwMXQxX2V2YWw='));//",
			# "\";exit(base64_decode('dzRwMXQxX2V2YWw='));#",
			# "';exit(base64_decode('dzRwMXQxX2V2YWw='));//",
			# "';exit(base64_decode('dzRwMXQxX2V2YWw='));#",
			# "\".exit(base64_decode('dzRwMXQxX2V2YWw='));//",
			# "\".exit(base64_decode('dzRwMXQxX2V2YWw='));#",
			# "'.exit(base64_decode('dzRwMXQxX2V2YWw='));//",
			# "'.exit(base64_decode('dzRwMXQxX2V2YWw='));#",
		]

	def signature(self):
		return {
			"Unsafe function preg_replace()": [
				"Fatal error</b>: preg_replace", # TODO check this signature
				"Warning: preg_replace():" # TODO add more signature
			],
			"Unsafe function eval()": [
				"eval()'d code</b> on line <b>",
				],
			"OS Command Injection": [
				"Cannot execute a blank command in",
				"sh: command substitution:",
				"PATH=",
				"PWD=",
			],
			"Unsafe function usort()": [
				"Warning: usort()",
			],
			"Unsafe function assert()": [
				"Warning: assert():",
			],
			"Code Evaluation": [
				"Failure evaluating code:",
				"w4p1t1_eval",
			]
		}
