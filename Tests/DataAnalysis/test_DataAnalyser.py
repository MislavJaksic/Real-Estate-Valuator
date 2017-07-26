from RealEstateValuationSystem.DataAnalysis.DataAnalyser import DataAnalyser

class TestDataAnalyser(object):
	def test_template(self):
		pass
	
	def test_LoadData(self):
		analyser = DataAnalyser()
		assert analyser.LoadDataset() == True
		
	def test_ReplaceListsWithValuesInDict(self):
		analyser = DataAnalyser()
		input = {'A' : [5], 'B' : [u'hi'], 'C' : None}
		output = {'A' : 5, 'B' : u'hi', 'C' : None}
		assert analyser.ReplaceListsWithValuesInDict(input) == output
		
	def test_CountValues(self):
		analyser = DataAnalyser()
		analyser.LoadDataset()
		assert analyser.CountValues() == True
		
	def test_CountMissingValues(self):
		analyser = DataAnalyser()
		analyser.LoadDataset()
		assert analyser.CountMissingValues() == True
		