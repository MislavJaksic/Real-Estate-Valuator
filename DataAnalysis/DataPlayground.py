from DatasetAnalyser import DatasetAnalyser
import DatasetConfig
import numpy

analyser = DatasetAnalyser()
analyser.LoadDataset()

analyser.KeepRows('size < 450') #all larger are a mistake
analyser.KeepRows('priceInEuros > 5000') #all who set smaller prices are manipulating it
analyser.LogTrans('priceInEuros')
analyser.LogTrans('size')
#analyser.DrawScatterGraphColumn('size')
#analyser.DrawDistributionGraphs()

#analyser.DrawBoxGraphColumn('floor')
#analyser.DrawBoxGraphColumn('place')
#analyser.DrawBoxGraphColumn('town')
#analyser.DrawBoxGraphColumn('numberOfRooms')


#analyser.DrawBoxGraphColumn('yearOfConstruction')
#analyser.DrawBoxGraphColumn('yearOfLastAdaptation')

#analyser.DrawBoxGraphColumn('sizeOfGarden')
#analyser.DrawBoxGraphColumn('sizeOfTerrace')
#analyser.DrawBoxGraphColumn('sizeOfBalcony')
#analyser.DrawBoxGraphColumn('numberOfParkingSpaces')

#for column in DatasetConfig.categoricalColumns:
#	analyser.DrawBoxGraphColumn(column)
#analyser.DropColumns()

#creates a new column 'isPenthouse' and sets value for each row: 1 if row has Penthouse, 0 otherwise
analyser.dataset['isPenthouse'] = numpy.where(analyser.dataset['floor'] == 'Penthouse', 1, 0)
#analyser.DrawBoxGraphColumn('isPenthouse')
analyser.dataset['notSuteren'] = numpy.where(analyser.dataset['floor'] != 'Suteren', 1, 0)
#analyser.DrawBoxGraphColumn('isSuteren')
analyser.dataset = analyser.dataset.replace({'numberOfRooms' : {"Garsonijera" : 1, "1-1.5 sobni" : 2, "2-2.5 sobni": 3, "3-3.5 sobni": 4, "4+": 5}})
#analyser.DrawBoxGraphColumn('numberOfRooms')
analyser.dataset['hasBalcony'] = numpy.where(analyser.dataset['sizeOfBalcony'] > 0, 1, 0)
analyser.dataset['hasGarden'] = numpy.where(analyser.dataset['sizeOfGarden'] > 0, 1, 0)
analyser.dataset['hasTerrace'] = numpy.where(analyser.dataset['sizeOfTerrace'] > 0, 1, 0)
analyser.dataset['hasParking'] = numpy.where(analyser.dataset['numberOfParkingSpaces'] > 0, 1, 0)

#analyser.DrawCorrelationMatrix()

# analyser.dataset.loc[analyser.dataset['sellerLink'].str.contains('korisnik'), 'sellerLink'] = 'K'
# analyser.dataset.loc[analyser.dataset['sellerLink'].str.contains('agencija'), 'sellerLink'] = 'A'
# analyser.dataset.loc[analyser.dataset['sellerLink'].str.contains('trgovina'), 'sellerLink'] = 'Tr'
# analyser.dataset.loc[analyser.dataset['sellerLink'].str.contains('tvrtka'), 'sellerLink'] = 'Tv'
# analyser.dataset.loc[analyser.dataset['sellerLink'].str.contains('investitor'), 'sellerLink'] = 'I'
# analyser.dataset.loc[analyser.dataset['sellerLink'].str.contains('obrt'), 'sellerLink'] = 'Ob'
# analyser.dataset.loc[analyser.dataset['sellerLink'].str.contains('webshop'), 'sellerLink'] = 'W'
# analyser.dataset.loc[analyser.dataset['sellerLink'].str.contains('oglasivac'), 'sellerLink'] = 'Og'

analyser.dataset['sellerLink'] = numpy.where(analyser.dataset['sellerLink'].str.contains('korisnik') == True, 1, 2)

analyser.DrawBoxGraphColumn('sellerLink', sortByMedian=True)

analyser.DrawCorrelationMatrix()

print analyser.dataset.columns.values
print 'hello'