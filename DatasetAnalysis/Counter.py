import sys
import os
sys.path.insert(0, os.path.abspath('../..'))

from RealEstateValuationSystem.InputControl.InputController import InputController

import pandas

def CountValues(dataset, dontCountColumns=[]):
	"""Counts the number of times a value occures in a column. Outputs the count to a .csv file to the
	same folder where this program is located. Returns True."""
	if not InputController.IsDataFrame(dataset):
		raise Exception("dataset is not a pandas DataFrame")
	if not InputController.IsList(dontCountColumns):
		raise Exception("dontCountColumns is not a list")
	
	savePath = os.path.abspath(__file__) + 'CountValues.csv'
	for columnName in dataset:
		if columnName in dontCountColumns:
			continue
		valueCount = dataset[columnName].value_counts()
		valueCount.to_csv(savePath, encoding='utf-8', mode='a', header=columnName)
	return True
	
def CountMissingValues(dataset):
	"""Counts the number of times a missing value (numpy.nan, Python None, 'missing', 'null') has occured
	in a column. Outputs the count to a .csv file to the same folder where this program is located.
	Returns True."""
	if not InputController.IsDataFrame(dataset):
		raise Exception("dataset is not a pandas DataFrame")
	
	nanSum = dataset.isnull().sum().sort_values(ascending=False)
	nanCount = dataset.isnull().count()
	nanPercent = (nanSum/nanCount).sort_values(ascending=False)
	nanData = pandas.concat([nanSum, nanPercent], axis=1, keys=['nanCount', 'nanPercent'])
	
	savePath = os.path.abspath(__file__) + 'MissingValues.csv'
	nanData.to_csv(savePath)
	return True