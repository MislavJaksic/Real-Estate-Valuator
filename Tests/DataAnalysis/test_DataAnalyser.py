from RealEstateValuationSystem.DataAnalysis.DatasetAnalyser import DatasetAnalyser

class TestDatasetAnalyser(object):
	def test_LoadData(self):
		analyser = DatasetAnalyser()
		assert analyser.LoadDataset() == True
		
	def test_ExtractValueFromListInDictT(self):
		analyser = DatasetAnalyser()
		input = {'A' : [5], 'B' : [u'hi'], 'C' : None}
		output = {'A' : 5, 'B' : u'hi', 'C' : None}
		assert analyser.ExtractValueFromListInDict(input) == output
		
	def test_ReplaceNaNValuesWithNanT(self):
		analyser = DatasetAnalyser()
		assert analyser.LoadDataset() == True
		assert analyser.ReplaceNaNValuesWithNan() == True
		
	def test_CountValuesT(self):
		analyser = DatasetAnalyser()
		analyser.LoadDataset()
		assert analyser.CountValues() == True
		
	def test_CountMissingValuesT(self):
		analyser = DatasetAnalyser()
		analyser.LoadDataset()
		assert analyser.CountMissingValues() == True
		
	def test_DrawSomething(self):
		pass
		