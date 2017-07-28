from RealEstateValuationSystem.DataAnalysis.DatasetAnalyser import DatasetAnalyser

class TestDatasetAnalyser(object):
	def test_template(self):
		pass
	
	def test_LoadData(self):
		analyser = DatasetAnalyser()
		assert analyser.LoadDataset() == True
		
	def test_ReplaceListsWithValuesInDictT(self):
		analyser = DatasetAnalyser()
		input = {'A' : [5], 'B' : [u'hi'], 'C' : None}
		output = {'A' : 5, 'B' : u'hi', 'C' : None}
		assert analyser.ReplaceListsWithValuesInDict(input) == output
		
	def test_ReplaceListsWithValuesInDictF(self):
		analyser = DatasetAnalyser()
		input = 'hello'
		output = {}
		assert analyser.ReplaceListsWithValuesInDict(input) == output
		
	def test_ReplaceNaNValuesWithNan(self):
		analyser = DatasetAnalyser()
		assert analyser.LoadDataset() == True
		assert analyser.ReplaceNaNValuesWithNan() == True
		
	def test_CountValues(self):
		analyser = DatasetAnalyser()
		analyser.LoadDataset()
		assert analyser.CountValues() == True
		
	def test_CountMissingValues(self):
		analyser = DatasetAnalyser()
		analyser.LoadDataset()
		assert analyser.CountMissingValues() == True
		