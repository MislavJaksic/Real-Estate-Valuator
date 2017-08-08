from RealEstateValuationSystem.DatasetSource import DatasetLoader
from RealEstateValuationSystem.DatasetAnalysis.ApartmentForSaleCollection import DatasetConfig
from RealEstateValuationSystem.DatasetAnalysis import Counter

import pytest

@pytest.fixture(scope='module')
def DatasetFunc():
	dataset = DatasetLoader.LoadFromMongoDB(DatasetConfig.conn)
	return dataset

def test_CountValues(DatasetFunc):
	assert (True == Counter.CountValues(DatasetFunc))

def test_CountMissingValues(DatasetFunc):
	assert (True == Counter.CountMissingValues(DatasetFunc))
