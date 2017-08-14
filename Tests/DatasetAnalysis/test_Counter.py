from RealEstateValuationSystem.DatasetSource import DatasetLoader
from RealEstateValuationSystem.DatasetAnalysis.ApartmentForSaleCollection import DatasetConfig
from RealEstateValuationSystem.DatasetAnalysis import Counter
import pytest
conn = {'database' : 'test', 'collection' : 'restaurants'}
cond = {'name' : u'Dj Reynolds Pub And Restaurant'}

@pytest.fixture(scope='module')
def DatasetFunc():
	dataset = DatasetLoader.Load(conn, cond)
	return dataset

def test_CountValues(DatasetFunc):
	assert (True == Counter.CountValues(DatasetFunc,
	                                    ['address', 'borough', 'cuisine', 'grades', 'name', 'restaurant_id']))

def test_CountMissingValues(DatasetFunc):
	assert (True == Counter.CountMissingValues(DatasetFunc))
