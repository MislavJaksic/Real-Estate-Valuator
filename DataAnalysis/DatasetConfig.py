ignoredColumns = [u'_id', u'adCode', u'adLink', u'adPublishedDate', u'objectCode']

target = u'priceInEuros'

uniqueColumns = [u'_id', u'adCode', u'adLink']

binaryColumns = [u'hasCargoElevator', u'hasElevator', u'isNewlyBuilt']

numericColumns = [u'adCode', u'numberOfParkingSpaces', u'priceInEuros', u'size', u'sizeOfBalcony',
                  u'sizeOfGarden', u'sizeOfTerrace', u'yearOfConstruction', u'yearOfLastAdaptation']

stringColumns = [u'_id', u'adLink', u'adPublishedDate', u'energyCertificate', u'floor', u'hasCargoElevator',
                 u'hasElevator', u'isNewlyBuilt', u'numberOfRooms', u'objectCode', u'place', u'sellerLink',
				 u'state', u'town', u'type']

nanValues = [0]