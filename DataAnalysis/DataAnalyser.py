import sys
import os
sys.path.insert(0, os.path.abspath('../..'))

from RealEstateValuationSystem.Database.Database import Database
from RealEstateValuationSystem.Database import DatabaseConfig
from RealEstateValuationSystem.InputControl.InputController import InputController
import DatasetConfig

import pandas
import numpy
import copy

class DataAnalyser(object):
	def __init__(self):
		self.data = []
	
	def LoadDataset(self):
		"""Load data into pandas DataFrame from the mongoDB collection. Always returns True."""
		db = Database()
		db.Open(DatabaseConfig.conn)
		
		iter = db.GetDataIter({})
		for doc in iter:
			doc = self.ReplaceListsWithValuesInDict(doc)
			self.data.append(doc)
		db.Close()
		
		self.data = pandas.DataFrame(self.data)
		return True
		
	def ReplaceListsWithValuesInDict(self, dict):
		"""Replace the pattern {'key1' : [value1], ...} with {'key1' : value1, ...}. All other values
		are left as it is."""
		for key in dict.keys():
			if InputController.IsList(dict[key]):
				dict[key] = dict[key][0]
		return dict
		
	def CountValues(self):
		"""Counts the number of times a value has occured in a column. Outputs the count to a .csv file.
		Always returns True."""
		for column in self.data:
			if column in DatasetConfig.ignoredColumns:
				continue
			count = self.data[column].value_counts()
			count.to_csv('CountValues.csv', encoding='utf-8', mode='a', header=column)
		return True
		
	def CountMissingValues(self):
		"""Counts the number of times a missing value has occured in a column. Outputs the count to
		a .csv file. Always returns True."""
		data = copy.deepcopy(self.data)
		for value in DatasetConfig.nanValues:
			data = data.replace(value, numpy.nan)
			
		nanSum = data.isnull().sum().sort_values(ascending=False)
		nanCount = data.isnull().count()
		nanPercent = (nanSum/nanCount).sort_values(ascending=False)
		nanData = pandas.concat([nanSum, nanPercent], axis=1, keys=['nanSum', 'nanPercent'])
		nanData.to_csv('MissingValues.csv')
		return True
		
	