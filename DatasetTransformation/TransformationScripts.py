import sys
import os
sys.path.insert(0, os.path.abspath('../..'))

import numpy

def MakeTransformationsForApartmentForSaleCollection(transformer):
	transformer.KeepRows('size < 450') #larger are outliers
	transformer.KeepRows('priceInEuros > 5000') #smaller prices are trying to manipulate rankings

	#careful! .loc cannot compare strings!!!

	floor = transformer.dataset['floor']
	transformer.dataset.loc[floor == 'Suteren', 'floor'] = 1
	transformer.dataset.loc[floor == 'Penthouse', 'floor'] = 3
	transformer.dataset.loc[(floor != 1) & (floor != 3), 'floor'] = 2
	transformer.dataset = transformer.dataset.astype({'floor' : int})

	#cargoEle = transformer.dataset['hasCargoElevator']
	#transformer.dataset.loc[cargoEle > 0, 'hasCargoElevator'] = 1
	#transformer.dataset = transformer.dataset.astype({'hasCargoElevator' : int})

	#transform place !!! !!! !!!
	
	parking = transformer.dataset['numberOfParkingSpaces']
	transformer.dataset = transformer.dataset.replace({'numberOfParkingSpaces' : {0 : 'none',
																			1 : 'some', 2 : 'some', 3 : 'some', 4 : 'some', 5 : 'some',
																			6 : 'lot', 7 : 'lot'}})
	transformer.dataset = transformer.dataset.replace({'numberOfParkingSpaces' : {'lot' : 1,
																			'none' : 2,
																			'some' : 2}})

	transformer.LogTransOnColumn('priceInEuros')
	transformer.LogTransOnColumn('size')

	transformer.dataset['sellerLink'] = numpy.where(transformer.dataset['sellerLink'].str.contains('korisnik') == True, 1, 2)
	
	return transformer
	
