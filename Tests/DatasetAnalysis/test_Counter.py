from RealEstateValuationSystem.DatasetSource import DatasetLoader
from RealEstateValuationSystem.DatasetAnalysis.ApartmentForSaleCollection import DatasetConfig
from RealEstateValuationSystem.DatasetAnalysis import Counter
import pytest
conn = {'database' : 'test', 'collection' : 'restaurants'}
cond = {'name' : u'Dj Reynolds Pub And Restaurant'}
dontCount = [u'borough', u'restaurant_id', u'grades', u'address', u'_id']

@pytest.fixture(scope='module')
def DatasetFunc():
	dataset = DatasetLoader.Load(conn, cond)
	return dataset

def test_CountValues(DatasetFunc):
	assert (True == Counter.CountValues(DatasetFunc, dontCount))

def test_CountMissingValues(DatasetFunc):
	assert (True == Counter.CountMissingValues(DatasetFunc))
