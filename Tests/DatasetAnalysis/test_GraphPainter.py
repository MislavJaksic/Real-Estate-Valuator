from RealEstateValuationSystem.DataAnalysis import DatasetLoader
from RealEstateValuationSystem.DataAnalysis import DatasetConfig
from RealEstateValuationSystem.DataAnalysis import GraphPainter

import pytest

@pytest.fixture(scope='module')
def DatasetFunc():
	dataset = DatasetLoader.LoadFromMongoDB(DatasetConfig.conn)
	return dataset
	
def test_DrawCorrelationMatrix(DatasetFunc):
	assert (True == GraphPainter.DrawCorrelationMatrix(DatasetFunc))
	
def test_DrawDistributionGraphs(DatasetFunc):
	assert (True == GraphPainter.DrawDistributionGraphs(DatasetFunc))
	
def test_DrawDistributionGraphColumn(DatasetFunc):
	assert (True == GraphPainter.DrawDistributionGraphColumn(DatasetFunc, 'priceInEuros'))
	
def test_DrawScatterGraphColumn(DatasetFunc):
	assert (True == GraphPainter.DrawScatterGraphColumn(DatasetFunc, 'priceInEuros', 'size'))
	
#def test_DrawBoxGraphs(DatasetFunc):
#	assert (True == GraphPainter.DrawBoxGraphs(DatasetFunc, 'priceInEuros'))
	
def test_DrawBoxGraphColumn(DatasetFunc):
	assert (True == GraphPainter.DrawBoxGraphColumn(DatasetFunc, 'priceInEuros', 'floor', sortByMedian=True))
	