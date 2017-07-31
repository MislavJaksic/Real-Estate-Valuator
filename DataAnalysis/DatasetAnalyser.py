import sys
import os
sys.path.insert(0, os.path.abspath('../..'))

from RealEstateValuationSystem.DatabaseControl.DatabaseController import DatabaseController
from RealEstateValuationSystem.InputControl.InputController import InputController
import DatasetConfig

import pandas
import numpy
import seaborn
import matplotlib.pyplot
import scipy.stats
import copy

class DatasetAnalyser(object):
	def __init__(self):
		self.dataset = []
	
	def LoadDataset(self):
		"""Load dataset into pandas DataFrame from the mongoDB collection. Always returns True."""
		db = DatabaseController()
		db.Open(DatasetConfig.conn)
		
		iter = db.GetDataIter({})
		for doc in iter:
			doc = self.ExtractValueFromListInDict(doc)
			self.dataset.append(doc)
		db.Close()
		
		self.dataset = pandas.DataFrame(self.dataset)
		return True
		
	def ExtractValueFromListInDict(self, dict):
		"""Replace the pattern {'key1' : [value1], ...} with {'key1' : value1, ...}. All other values
		are left as it is. Returns the extracted dictionary or raises an exception."""
		if not InputController.IsDict(dict):
			raise Exception("Cannot extract values because the parameter isn't a dictionary")
		
		for key in dict.keys():
			if InputController.IsList(dict[key]):
				dict[key] = dict[key][0]
		return dict
		
	def ReplaceNaNValuesWithNan(self):
		"""Replace values that have been declared NaN values with numpy.nan in the dataset. Returns True
		if the operation has been completed successfully, otherwise it returns False."""
		if not InputController.IsDataFrame(self.dataset):
			raise Exception("Dataset has not been loaded. Load it using .LoadDataset()")
		
		for value in DatasetConfig.nanValues:
			self.dataset = self.dataset.replace(value, numpy.nan)
		return True
		
	def CountValues(self):
		"""Counts the number of times a value has occured in a column. Outputs the count to a .csv file.
		Returns True if the operation has been completed successfully, otherwise it raises an exception."""
		if not InputController.IsDataFrame(self.dataset):
			raise Exception("Dataset has not been loaded. Load it using .LoadDataset()")
		
		for column in self.dataset:
			if column in DatasetConfig.ignoredColumns:
				continue
			count = self.dataset[column].value_counts()
			count.to_csv('CountValues.csv', encoding='utf-8', mode='a', header=column)
		return True
		
	def CountMissingValues(self):
		"""Counts the number of times a missing value has occured in a column. Outputs the count to
		a .csv file. Returns True if the operation has been completed successfully, otherwise it
		raises an exception."""
		if not InputController.IsDataFrame(self.dataset):
			raise Exception("Dataset has not been loaded. Load it using .LoadDataset()")
		
		self.ReplaceNaNValuesWithNan()
		nanSum = self.dataset.isnull().sum().sort_values(ascending=False)
		nanCount = self.dataset.isnull().count()
		nanPercent = (nanSum/nanCount).sort_values(ascending=False)
		nanData = pandas.concat([nanSum, nanPercent], axis=1, keys=['nanSum', 'nanPercent'])
		nanData.to_csv('MissingValues.csv')
		return True
		
	def DrawCorrelationMatrix(self):
		"""Plots the correlation between numerical columns. Ignores all other columns. Returns True
		if the operation has been completed successfully, otherwise it raises an exception."""
		if not InputController.IsDataFrame(self.dataset):
			raise Exception("Dataset has not been loaded. Load it using .LoadDataset()")
			
		corrmat = self.dataset.corr()
		f, ax = matplotlib.pyplot.subplots(figsize=(12, 9))
		seaborn.heatmap(corrmat, square=True)
		matplotlib.pyplot.xticks(rotation=90)
		matplotlib.pyplot.yticks(rotation=0)
		seaborn.plt.show()
		return True
		
	def DrawDistributionGraphs(self):
		"""Plots histograms of all .numericalColumns. Returns True if the operation has been
		completed successfully, otherwise it raises an exception."""
		if not InputController.IsDataFrame(self.dataset):
			raise Exception("Dataset has not been loaded. Load it using .LoadDataset()")
		
		f = pandas.melt(self.dataset, value_vars=DatasetConfig.numericalColumns)
		g = seaborn.FacetGrid(f, col="variable",  col_wrap=2, sharex=False, sharey=False)
		g = g.map(seaborn.distplot, "value")
		seaborn.plt.show()
		return True
		
	def DrawDistributionGraphColumn(self, column):
		"""Draw a column of a single numerical column. Returns True if the operation has been
		completed successfully, otherwise it raises an exception."""
		if not InputController.IsDataFrame(self.dataset):
			raise Exception("Dataset has not been loaded. Load it using .LoadDataset()")
			
		seaborn.distplot(self.dataset[column])
		seaborn.plt.show()
		return True
		
	def DrawScatterGraphColumn(self, column):
		"""Plots a scatter graph againt a .targetColumn. Plots only numerical columns. Returns True
		if the operation has been completed successfully, otherwise it raises an exception."""
		if not InputController.IsDataFrame(self.dataset):
			raise Exception("Dataset has not been loaded. Load it using .LoadDataset()")
			
		dataset = pandas.concat([self.dataset[DatasetConfig.target], self.dataset[column]], axis=1)
		dataset.plot.scatter(x=column, y=DatasetConfig.target)
		seaborn.plt.show()
		return True
		
	def DrawBoxGraphs(self):
		"""Plots box graphs (or box and wiskers plots) againt the .targetColumn. For comparing numerical
		and .categoricalColumns. Box shows the quartiles of the dataset, dots represent outliers and
		wiskers show the rest of the distribution. Returns True if the operation has been completed
		successfully, otherwise it raises an exception."""
		if not InputController.IsDataFrame(self.dataset):
			raise Exception("Dataset has not been loaded. Load it using .LoadDataset()")
		
		f = pandas.melt(self.dataset, id_vars=[DatasetConfig.target], value_vars=DatasetConfig.categoricalColumns)
		g = seaborn.FacetGrid(f, col="variable",  col_wrap=2, sharex=False, sharey=False, size=5)
		def boxplot(x, y, **kwargs):
			seaborn.boxplot(x=x, y=y)
			x=matplotlib.pyplot.xticks(rotation=90)
		g = g.map(boxplot, "value", DatasetConfig.target)
		seaborn.plt.show()
		return True
		
	def DrawBoxGraphColumn(self, column, sortByMedian=False):
		"""Plots a box graph of a categorical column againt the .targetColumn. Returns True if
		the operation has been completed successfully, otherwise it raises an exception."""
		if not InputController.IsDataFrame(self.dataset):
			raise Exception("Dataset has not been loaded. Load it using .LoadDataset()")
			
		data = pandas.concat([self.dataset[DatasetConfig.target], self.dataset[column]], axis=1)
		f, ax = matplotlib.pyplot.subplots(figsize=(8, 6))
		if sortByMedian:
			sortedIndexes = data.groupby([column]).median().sort_values([DatasetConfig.target]).index
			fig = seaborn.boxplot(x=column, y=DatasetConfig.target, data=data, order=sortedIndexes)
		else:
			fig = seaborn.boxplot(x=column, y=DatasetConfig.target, data=data)
		matplotlib.pyplot.xticks(rotation=90)
		seaborn.plt.show()
		return True
		
	def LogTrans(self, column):
		"""Applies a logarithm to all values in a column. Use to create normality when the skewness
		is positive (leaning towards left)."""
		if not InputController.IsDataFrame(self.dataset):
			raise Exception("Dataset has not been loaded. Load it using .LoadDataset()")
			
		self.dataset[column] = numpy.log1p(self.dataset[column])
		return True
		
	def DropColumns(self):
		"""Drops .dropColumns from the dataset. Use either when there is a lot of missing data or
		the data is irrelevant."""
		if not InputController.IsDataFrame(self.dataset):
			raise Exception("Dataset has not been loaded. Load it using .LoadDataset()")
		
		self.dataset = self.dataset.drop(DatasetConfig.dropColumns, axis=1)
		return True
		
	def KeepRows(self, condition):
		"""Actually used to drop outliers, rows with extreme values or mistakes. Condition has to be a string
		such as 'a > b' as it will then be transplated into (d[a] > d[b])."""
		if not InputController.IsDataFrame(self.dataset):
			raise Exception("Dataset has not been loaded. Load it using .LoadDataset()")
			
		self.dataset = self.dataset.query(condition)
		return True
		