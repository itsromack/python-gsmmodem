class Person:
	""" A person class """
	first_name = ""
	last_name = ""
	mobile_number = ""
	code_name = ""

	def __init__(self, first_name, last_name, mobile_number, code_name):
		self.first_name = first_name
		self.last_name = last_name
		self.mobile_number = mobile_number
		self.code_name = code_name
	
	def get_full_name(self):
		return "%s %s" % self.first_name, self.last_name
