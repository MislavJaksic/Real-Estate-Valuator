import sys
import os
sys.path.insert(0, os.path.abspath('../..'))

from RealEstateValuationSystem.InputControl.InputController import InputController

import numpy

class DatasetTransformer(object):
	def __init__(self, pandasDataFrame):
		if not InputController.IsDataFrame(pandasDataFrame):
			raise Exception("pandasDataFrame is not a pandas DataFrame")
		self.dataset = pandasDataFrame
		
	def InspectDataset(self):
		print "Column names:"
		print self.dataset.columns.values
		
		print "DTypes (defined by numpy):"
		print self.dataset.dtypes
		
		print "Numeric columns:"
		print list(self.dataset.select_dtypes(include=[numpy.number]).columns)
		
		print "Categoric columns:"
		print list(self.dataset.select_dtypes(include=[numpy.object_]).columns)
		
		print "Describe numeric columns:"
		print self.dataset.describe()
		
		print "Data sample (first 10 rows):"
		print self.dataset.head(10)
		return True
	
	def ReplaceNaNValuesWithNan(self, nanValues):
		"""Replace nanValues with numpy.nan values."""
		if not InputController.IsList(nanValues):
			raise Exception("nanValues should be a list")
		
		for value in nanValues:
			self.dataset = self.dataset.replace(value, numpy.nan)
		return True
		
	def LogTransOnColumn(self, column):
		"""Apply a natural logarithm to all values in a column. Use to create normality when the
		skewness is positive (leaning towards left)."""
		self.dataset[column] = numpy.log1p(self.dataset[column])
		return True
		
	def DropColumns(self, columns):
		"""Drop columns from the dataset. Use either when there is a lot of missing data or
		the data is irrelevant."""
		if not InputController.IsList(columns):
			raise Exception("columns should be a list")
		
		self.dataset = self.dataset.drop(columns, axis=1)
		return True
		
	def KeepRows(self, condition):
		"""Used for eliminating outliers, rows with extreme values or mistakes. Condition has to be a string
		such as 'a > b' as it will then be translated into (d[a] > d[b])."""		
		self.dataset = self.dataset.query(condition)
		return True
		
	# def ReplaceValueWithValueInColumn(self, value, replacementValue, column):
		# """"""
		# self.dataset.loc[self.dataset[column] == value, column] = replacementValue
		# return True
		