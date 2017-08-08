from RealEstateValuationSystem.DataAnalysis import DatasetLoader
from RealEstateValuationSystem.InputControl.InputController import InputController
from RealEstateValuationSystem.DataAnalysis import DatasetConfig

def test_FromMongoDB():
	dataset = DatasetLoader.LoadFromMongoDB(DatasetConfig.conn)
	assert (True == InputController.IsDataFrame(dataset))
	
def test_ExtractValueFromListInDict():
	input = {1 : ['A']}
	output = {1 : 'A'}
	assert (output == DatasetLoader.ExtractValueFromListInDict(input))