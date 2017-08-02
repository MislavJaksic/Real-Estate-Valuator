from DatasetAnalyser import DatasetAnalyser
import DatasetConfig

import DatasetConfig
import numpy
import pandas

analyser = DatasetAnalyser()
analyser.LoadDataset(DatasetConfig.conn)

analyser.KeepRows('size < 450') #larger are outliers
analyser.KeepRows('priceInEuros > 5000') #smaller prices are trying to manipulate rankings
#analyser.DrawScatterGraphColumn('size')

#careful! .loc cannot compare strings!!!

floor = analyser.dataset['floor']
analyser.dataset.loc[floor == 'Suteren', 'floor'] = 1
analyser.dataset.loc[floor == 'Penthouse', 'floor'] = 3
analyser.dataset.loc[(floor != 1) & (floor != 3), 'floor'] = 2
analyser.dataset = analyser.dataset.astype({'floor' : int})
#analyser.DrawBoxGraphColumn('floor')

cargoEle = analyser.dataset['hasCargoElevator']
analyser.dataset.loc[cargoEle > 0, 'hasCargoElevator'] = 1
analyser.dataset = analyser.dataset.astype({'hasCargoElevator' : int})
#analyser.DrawBoxGraphColumn('hasCargoElevator')

#transform place !!! !!! !!!

#analyser.DrawBoxGraphColumn('numberOfParkingSpaces')
parking = analyser.dataset['numberOfParkingSpaces']
analyser.dataset = analyser.dataset.replace({'numberOfParkingSpaces' : {0 : 'none',
                                                                        1 : 'some', 2 : 'some', 3 : 'some', 4 : 'some', 5 : 'some',
																		6 : 'lot', 7 : 'lot'}})
analyser.dataset = analyser.dataset.replace({'numberOfParkingSpaces' : {'lot' : 1,
                                                                        'none' : 2,
																		'some' : 2}})
#analyser.DrawBoxGraphColumn('numberOfParkingSpaces')

#analyser.DrawBoxGraphColumn('yearOfConstruction')
#analyser.DrawBoxGraphColumn('yearOfLastAdaptation')

analyser.LogTrans('priceInEuros')
analyser.LogTrans('size')
#analyser.DrawDistributionGraphColumn('priceInEuros')
#analyser.DrawDistributionGraphColumn('size')

analyser.dataset['sellerLink'] = numpy.where(analyser.dataset['sellerLink'].str.contains('korisnik') == True, 1, 2)

analyser.DropColumns(DatasetConfig.dropColumns)

print analyser.dataset.columns.values
print analyser.dataset.describe()
print analyser.dataset.head()
print analyser.dataset.dtypes
analyser.DrawCorrelationMatrix()
