from RealEstateValuationSystem.InputControl.InputController import InputController

class TestInputController(object):
	def test_IsDict(self):
		dict = {'A' : 1}
		assert InputController.IsDict(dict) == True
		
	def test_IsBool(self):
		boolean = True
		assert InputController.IsBool(boolean) == True
		
	def test_IsList(self):
		list = []
		assert InputController.IsList(list) == True
		
	def test_IsDataFrame(self):
		list = []
		assert InputController.IsDataFrame(list) == False
		