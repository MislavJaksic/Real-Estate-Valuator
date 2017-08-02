from RealEstateValuationSystem.DataAnalysis.DatasetAnalyser import DatasetAnalyser
from RealEstateValuationSystem.DataAnalysis import DatasetConfig

class TestDatasetAnalyser(object):
	def test_LoadData(self):
		analyser = DatasetAnalyser()
		assert analyser.LoadDataset(DatasetConfig.conn) == True
		
	def test_ExtractValueFromListInDictT(self):
		analyser = DatasetAnalyser()
		input = {'A' : [5], 'B' : [u'hi'], 'C' : None}
		output = {'A' : 5, 'B' : u'hi', 'C' : None}
		assert analyser.ExtractValueFromListInDict(input) == output
		
	def test_ReplaceNaNValuesWithNanT(self):
		analyser = DatasetAnalyser()
		analyser.LoadDataset(DatasetConfig.conn)
		assert analyser.ReplaceNaNValuesWithNan(DatasetConfig.nanValues) == True
		
	def test_CountValuesT(self):
		analyser = DatasetAnalyser()
		analyser.LoadDataset(DatasetConfig.conn)
		assert analyser.CountValues() == True
		
	def test_CountMissingValuesT(self):
		analyser = DatasetAnalyser()
		analyser.LoadDataset(DatasetConfig.conn)
		assert analyser.CountMissingValues() == True
		
	def test_DrawSomething(self):
		pass
		