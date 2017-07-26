import types

class InputController(object):
	
	@staticmethod
	def IsDict(param):
		"""Checks if the paramater is a dictionary. Returns True if it is, False if it is not."""
		if type(param) is types.DictType:
			return True
		return False

	@staticmethod
	def IsBool(param):
		"""Checks if the paramater is a boolean value. Returns True if it is, False if it is not."""
		if type(param) is types.BooleanType:
			return True
		return False
		
	@staticmethod
	def IsList(param):
		"""Checks if the paramater is a boolean value. Returns True if it is, False if it is not."""
		if type(param) is types.ListType:
			return True
		return False