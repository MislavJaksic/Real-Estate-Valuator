from RealEstateValuationSystem.DatasetSource import DatasetLoader
from RealEstateValuationSystem.InputControl.InputController import InputController
conn = {'database' : 'test', 'collection' : 'restaurants'}

def test_FromMongoDB():
	dataset = DatasetLoader.LoadFromMongoDB(conn)
	assert (True == InputController.IsDataFrame(dataset))
	
def test_ExtractValueFromListInDict():
	input = {1 : ['A']}
	output = {1 : 'A'}
	assert (output == DatasetLoader.ExtractValueFromListInDict(input))
