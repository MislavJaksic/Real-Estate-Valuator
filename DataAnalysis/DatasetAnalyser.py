import sys
import os
sys.path.insert(0, os.path.abspath('../..'))

from RealEstateValuationSystem.Database.Database import Database
from RealEstateValuationSystem.Database import DatabaseConfig
from RealEstateValuationSystem.InputControl.InputController import InputController
import DatasetConfig

import pandas
import numpy
import seaborn
import matplotlib.pyplot
import copy

class DatasetAnalyser(object):
	def __init__(self):
		self.dataset = []
	
	def LoadDataset(self):
		"""Load dataset into pandas DataFrame from the mongoDB collection. Always returns True."""
		db = Database()
		db.Open(DatabaseConfig.conn)
		
		iter = db.GetDataIter({})
		for doc in iter:
			doc = self.ReplaceListsWithValuesInDict(doc)
			self.dataset.append(doc)
		db.Close()
		
		self.dataset = pandas.DataFrame(self.dataset)
		self.ReplaceNaNValuesWithNan()
		return True
		
	def ReplaceListsWithValuesInDict(self, dict):
		"""Replace the pattern {'key1' : [value1], ...} with {'key1' : value1, ...}. All other values
		are left as it is. Returns the extracted dictionary."""
		if not InputController.IsDict(dict):
			return {}
		
		for key in dict.keys():
			if InputController.IsList(dict[key]):
				dict[key] = dict[key][0]
		return dict
		
	def ReplaceNaNValuesWithNan(self):
		""""""
		for value in DatasetConfig.nanValues:
			self.dataset = self.dataset.replace(value, numpy.nan)
		return True
		
	def CountValues(self):
		"""Counts the number of times a value has occured in a column. Outputs the count to a .csv file.
		Always returns True."""
		for column in self.dataset:
			if column in DatasetConfig.ignoredColumns:
				continue
			count = self.dataset[column].value_counts()
			count.to_csv('CountValues.csv', encoding='utf-8', mode='a', header=column)
		return True
		
	def CountMissingValues(self):
		"""Counts the number of times a missing value has occured in a column. Outputs the count to
		a .csv file. Always returns True."""
		nanSum = self.dataset.isnull().sum().sort_values(ascending=False)
		nanCount = self.dataset.isnull().count()
		nanPercent = (nanSum/nanCount).sort_values(ascending=False)
		nanData = pandas.concat([nanSum, nanPercent], axis=1, keys=['nanSum', 'nanPercent'])
		nanData.to_csv('MissingValues.csv')
		return True
		
	def CorrelationMatrix(self):
		"""Plots the correlation between numerical dataset. Ignores all other dataset in the DataFrame.
		Always return True."""
		corrmat = self.dataset.corr()
		f, ax = matplotlib.pyplot.subplots(figsize=(12, 9))
		seaborn.heatmap(corrmat, square=True)
		seaborn.plt.show()
		return True
		
	def DistributionGraph(self, column):
		"""Plots a histogram and overlaps it with a distribution curve. Always return True."""
		print "Skewness: ",
		print self.dataset[column].skew()
		print "Kurtosis: ",
		print self.dataset[column].kurt()
		seaborn.distplot(self.dataset[column])
		seaborn.plt.show()
		return True
		
	def ScatterGraph(self, column):
		"""HAS problem with non numerical... check it out"""
		dataset = pandas.concat([self.dataset[DatasetConfig.target], self.dataset[column]], axis=1)
		dataset.plot.scatter(x=column, y=DatasetConfig.target)
		seaborn.plt.show()
		return True
		