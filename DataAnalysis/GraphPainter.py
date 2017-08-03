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


	
def DrawCorrelationMatrix(dataset):
	"""Plots the correlation between columns which pandas considers numerical (use .dtypes to find out).
	Returns True and displays a graph."""
	if not InputController.IsDataFrame(dataset):
		raise Exception("dataset is not a pandas DataFrame")
		
	corrmat = dataset.corr()
	f, ax = matplotlib.pyplot.subplots(figsize=(12, 9))
	seaborn.heatmap(corrmat, square=True)
	matplotlib.pyplot.xticks(rotation=90)
	matplotlib.pyplot.yticks(rotation=0)
	seaborn.plt.show()
	return True
	
def DrawDistributionGraphs(dataset):
	"""Plots histograms of all numeric columns. Returns True and displays a graph."""
	if not InputController.IsDataFrame(dataset):
		raise Exception("dataset is not a pandas DataFrame")
	
	numericColumns = list(dataset.select_dtypes(include=[numpy.number]).columns)
	f = pandas.melt(dataset, value_vars=numericColumns)
	g = seaborn.FacetGrid(f, col="variable",  col_wrap=2, sharex=False, sharey=False)
	g = g.map(seaborn.distplot, "value")
	seaborn.plt.show()
	return True
	
def DrawDistributionGraphColumn(dataset, column):
	"""Draw a column of a single numeric column. Returns True and displays a graph."""
	if not InputController.IsDataFrame(dataset):
		raise Exception("dataset is not a pandas DataFrame")
		
	seaborn.distplot(dataset[column])
	seaborn.plt.show()
	return True
	
def DrawScatterGraphColumn(dataset, columnY, columnX):
	"""Two variables are plotted against each other on a scatter graph. Returns True and displays a graph."""
	if not InputController.IsDataFrame(dataset):
		raise Exception("dataset is not a pandas DataFrame")
		
	dataset = pandas.concat([dataset[columnY], dataset[columnX]], axis=1)
	dataset.plot.scatter(x=columnX, y=columnY)
	seaborn.plt.show()
	return True
	#takes a long time to perform, don't use it
def DrawBoxGraphs(dataset, columnY):
	"""Plots box graphs (or box and wiskers plots) againt a column. For comparing a numeric and categoric
	variables. The box shows the quartiles of the dataset, dots represent outliers and
	wiskers show the rest of the distribution. Returns True and displays a graph."""
	if not InputController.IsDataFrame(dataset):
		raise Exception("dataset is not a pandas DataFrame")
	
	categoricColumns = list(dataset.select_dtypes(include=[numpy.object_]).columns)
	f = pandas.melt(dataset, id_vars=[columnY], value_vars=categoricColumns)
	g = seaborn.FacetGrid(f, col="variable",  col_wrap=2, sharex=False, sharey=False, size=5)
	def boxplot(x, y, **kwargs):
		seaborn.boxplot(x=x, y=y)
		x=matplotlib.pyplot.xticks(rotation=90)
	g = g.map(boxplot, "value", columnY)
	seaborn.plt.show()
	return True
	
def DrawBoxGraphColumn(dataset, columnY, columnX, sortByMedian=False):
	"""Two variables are plotted against each other on a box graph. Returns True and displays a graph."""
	if not InputController.IsDataFrame(dataset):
		raise Exception("dataset is not a pandas DataFrame")
		
	data = pandas.concat([dataset[columnY], dataset[columnX]], axis=1)
	f, ax = matplotlib.pyplot.subplots(figsize=(8, 6))
	if sortByMedian:
		sortedIndexes = data.groupby([columnX]).median().sort_values([columnY]).index
		fig = seaborn.boxplot(x=columnX, y=columnY, data=data, order=sortedIndexes)
	else:
		fig = seaborn.boxplot(x=columnX, y=columnY, data=data)
	matplotlib.pyplot.xticks(rotation=90)
	seaborn.plt.show()
	return True