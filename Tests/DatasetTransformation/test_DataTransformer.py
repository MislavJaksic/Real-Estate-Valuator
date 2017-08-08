from RealEstateValuationSystem.DataAnalysis.DatasetTransformer import DatasetTransformer
from RealEstateValuationSystem.DatasetSource import DatasetLoader
from RealEstateValuationSystem.DatasetAnalysis.ApartmentForSaleCollection import DatasetConfig

import pytest

class TestDatasetTransformer(object):
	@pytest.fixture(scope='class')
	def TransformerFunc(self):
		dataset = DatasetLoader.LoadFromMongoDB(DatasetConfig.conn)
		transformer = DatasetTransformer(dataset)
		return transformer
		
	def test_ReplaceNaNValuesWithNanT(self, TransformerFunc):
		assert TransformerFunc.ReplaceNaNValuesWithNan(DatasetConfig.nanValues) == True
		
	def test_LogTransOnColumn(self, TransformerFunc):
		assert TransformerFunc.LogTransOnColumn('size') == True
		
	def test_DropColumns(self, TransformerFunc):
		assert TransformerFunc.DropColumns(['_id']) == True
		
	def test_KeepRows(self, TransformerFunc):
		assert TransformerFunc.KeepRows('priceInEuros > 5000') == True
	
#	def test_ReplaceValueWithValueInColumn(self, TransformerFunc):
#		assert TransformerFunc.ReplaceValueWithValueInColumn() == True
		
