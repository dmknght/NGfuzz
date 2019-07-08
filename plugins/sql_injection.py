import re

class Check(object):
	def __init__(self):
		self.payload = self.gen_payload()
		self.sig = {
			"MySQL Injection": [
				"You have an error in your SQL syntax",
				"supplied argument is not a valid MySQL"
			],
			"Java SQL Injection": [
				"java.sql.SQLException: Syntax error or access violation",
				"java.sql.SQLException: Unexpected end of command"
				],
			"PostgreSQL Injection": [
				"PostgreSQL query failed: ERROR: parser:",
			],
			"XPathException": [
				"XPathException",
				"Warning: SimpleXMLElement::xpath():"
			],
			"MSSQL Injection": [
				"[Microsoft][ODBC SQL Server Driver]",
				"Microsoft OLE DB Provider for ODBC Drivers</font> <font size=\"2\" face=\"Arial\">error",
				"Microsoft OLE DB Provider for ODBC Drivers",
			],
			"MSAccess SQL Injection": [
				"[Microsoft][ODBC Microsoft Access Driver]",
			],
			"LDAP Injection": [
				"supplied argument is not a valid ldap",
				"javax.naming.NameNotFoundException"
			],
			"DB2 Injection": [
				"DB2 SQL error:"
			],
			"Interbase Injection": [
				"Dynamic SQL Error",
			],
			"Sybase Injection" : [
				 "Sybase message:",
			],
			".NET SQL Injection" : [
				"Unclosed quotation mark after the character string",
			],
		}

	def check(self, browser):
		response = str(browser.get_current_page())
		for injection_types in self.sig.keys():
			for sig in self.sig[injection_types]:
				match = re.findall(re.escape(sig), response)
				if match:
					self.found(injection_types, browser.get_url())
					return True

	def gen_payload(self):
		return ["'"]

	def found(self, inject_type, url):
		events.vulnerable(inject_type, url)
