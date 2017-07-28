from DataAnalyser import DataAnalyser

analyser = DataAnalyser()
analyser.LoadDataset()
print analyser.data.columns.values
print analyser.data.describe()
#analyser.CorrelationMatrix()
#analyser.DistributionGraph('priceInEuros')
analyser.ScatterGraph(u'size')
print 'hello'