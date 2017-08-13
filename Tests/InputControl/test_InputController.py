from RealEstateValuationSystem.InputControl.InputController import InputController
import pandas

class TestInputController(object):
	def test_IsDictT(self):
		dict = {'A' : 1}
		assert InputController.IsDict(dict) == True
		
	def test_IsDictF(self):
		list = []
		assert InputController.IsDict(dict) == False
		
	def test_IsBoolT(self):
		boolean = True
		assert InputController.IsBool(boolean) == True
		
	def test_IsBoolF(self):
		dict = {}
		assert InputController.IsBool(dict) == False
		
	def test_IsListT(self):
		list = []
		assert InputController.IsList(list) == True
		
	def test_IsListF(self):
		boolean = False
		assert InputController.IsList(boolean) == False
		
	def test_IsDataFrameT(self):
		frame = pandas.DataFrame()
		assert InputController.IsDataFrame(frame) == True
		
	def test_IsDataFrameF(self):
		list = []
		assert InputController.IsDataFrame(list) == False
		
	def test_IsStringT(self):
		string = 'string'
		assert InputController.IsString(string) == True
		
	def test_IsStringF(self):
		list = []
		assert InputController.IsString(list) == False
		