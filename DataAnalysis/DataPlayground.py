from DatasetAnalyser import DatasetAnalyser
import DatasetConfig

analyser = DatasetAnalyser()
analyser.LoadDataset()

#analyser.DropColumns()
analyser.KeepRows('size < 450') #all larger are a mistake
analyser.KeepRows('priceInEuros > 5000') #all who set smaller prices are manipulating it
analyser.LogTrans('priceInEuros')
analyser.LogTrans('size')
#analyser.DrawScatterGraphColumn('size')
#analyser.DrawDistributionGraphs()
#analyser.DrawBoxGraphColumn('yearOfConstruction')
analyser.DrawBoxGraphColumn('yearOfLastAdaptation')
#for column in DatasetConfig.categoricalColumns:
#	analyser.DrawBoxGraphColumn(column)
print analyser.dataset.columns
print 'hello'