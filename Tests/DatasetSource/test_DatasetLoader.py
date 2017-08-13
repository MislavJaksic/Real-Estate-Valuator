from RealEstateValuationSystem.DatasetSource import DatasetLoader
from RealEstateValuationSystem.InputControl.InputController import InputController
import pytest
conn = {'database' : 'test', 'collection' : 'restaurants'}
cond = {'name' : u'Dj Reynolds Pub And Restaurant'}

def test_LoadDB():
	dataset = DatasetLoader.Load(conn, cond)
	assert dataset['name'][0] == u'Dj Reynolds Pub And Restaurant'
	
def test_LoadF():
	dataset = DatasetLoader.Load('ApartmentsForSale', {})
	assert InputController.IsDataFrame(dataset) == True

def test_LoadFromMongoDB():
	dataset = DatasetLoader._LoadFromMongoDB(conn, cond)
	assert dataset['name'][0] == u'Dj Reynolds Pub And Restaurant'
	
def test_LoadFromMongoDBE():
	with pytest.raises(Exception) as e_info:
		db._LoadFromMongoDB('wrong', {})
		
def test_LoadFromMongoDBAE():
	with pytest.raises(Exception) as e_info:
		db._LoadFromMongoDB({}, 'wrong')
	
def test_ExtractValueFromListInDict():
	input = {1 : ['A']}
	output = {1 : 'A'}
	assert DatasetLoader._ExtractValueFromListInDict(input) == output
	
def test_ExtractValueFromListInDictE():
	with pytest.raises(Exception) as e_info:
		db._ExtractValueFromListInDict('wrong')
