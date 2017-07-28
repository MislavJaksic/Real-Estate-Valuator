#ignored columns don't have their values occurences counted
ignoredColumns = [u'_id', u'adCode', u'adLink', u'adPublishedDate', u'objectCode']
#binary columns have a yes or no value
binaryColumns = [u'hasCargoElevator', u'hasElevator', u'isNewlyBuilt']
#target is the column that will be predicted
#used in drawing box and scatter graphs
target = u'priceInEuros'
#values that represent null, None and Missing in the dataset
nanValues = [0]
#which columns should be dropped
dropColumns = [u'energyCertificate', u'hasCargoElevator', u'hasElevator', u'isNewlyBuilt', u'state', u'type']
#-.-.-.-.- #columns are either unique, numerical and categorical #-.-.-.-.-
#unique columns have a very large number of unique values
uniqueColumns = [u'_id', u'adCode', u'adLink', u'adPublishedDate', u'objectCode', u'sellerLink']
#numerical values have floats, decimals or integers for values
#used in drawing distribution graphs
numericalColumns = [u'adCode', u'numberOfParkingSpaces', u'priceInEuros', u'size', u'sizeOfBalcony',
                    u'sizeOfGarden', u'sizeOfTerrace', u'yearOfConstruction', u'yearOfLastAdaptation']
#categorical values have strings or similar category values
#used in drawing box graphs
categoricalColumns = [u'energyCertificate', u'floor',
                      u'hasCargoElevator', u'hasElevator', u'isNewlyBuilt', u'numberOfRooms',
					  u'place', u'state', u'town', u'type']