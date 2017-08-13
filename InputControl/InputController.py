import types
import pandas

class InputController(object):
	@staticmethod
	def IsDict(param):
		"""Checks if the paramater is a dictionary."""
		if type(param) is types.DictType:
			return True
		return False

	@staticmethod
	def IsBool(param):
		"""Checks if the paramater is a boolean value."""
		if type(param) is types.BooleanType:
			return True
		return False
		
	@staticmethod
	def IsList(param):
		"""Checks if the paramater is a list."""
		if type(param) is types.ListType:
			return True
		return False
		
	@staticmethod
	def IsDataFrame(param):
		"""Checks if the paramater is a pandas DataFrame."""
		if type(param) is type(pandas.DataFrame()):
			return True
		return False
	
	@staticmethod
	def IsString(param):
		"""Checks if the paramater is a string."""
		if type(param) is types.StringType:
			return True
		return False
		
		
		