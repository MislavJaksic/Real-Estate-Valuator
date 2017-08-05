import sys
import os
sys.path.insert(0, os.path.abspath('../..'))

from RealEstateValuationSystem.DataAnalysis import DatasetConfig
from RealEstateValuationSystem.DataAnalysis.DatasetTransformer import DatasetTransformer
from RealEstateValuationSystem.DataAnalysis import DatasetLoader
from RealEstateValuationSystem.DataAnalysis import TransformationScripts

from sklearn.linear_model import LinearRegression, ElasticNet, ElasticNetCV
from sklearn.model_selection import GridSearchCV
from sklearn.feature_selection import SelectKBest, f_regression, RFECV
from sklearn.ensemble import GradientBoostingRegressor
import numpy
import pandas


def PredictIntervalValue(customerApartment):
	dataset = DatasetLoader.LoadFromMongoDB(DatasetConfig.conn)
	
	#insert dummy data to prevent it from being dropped or being incomplete
	customerApartment['priceInEuros'] = [100000]
	customerApartment['sellerLink'] = [u'/korisnik/']
	print customerApartment
	print dataset.tail()
	cutomerApartmentPandas = pandas.DataFrame(customerApartment)
	dataset = pandas.concat([dataset, cutomerApartmentPandas], ignore_index=True)
	print dataset.tail()
	
	transformer = DatasetTransformer(dataset)
	transformer.DropColumns(DatasetConfig.dropColumns)
	
	TransformationScripts.MakeTransformationsForApartmentForSaleCollection(transformer)
	
	print transformer.dataset.tail()
	
	Y = transformer.dataset['priceInEuros']
	transformer.DropColumns(['priceInEuros', 'place', 'town'])
	X = transformer.dataset
	#pd.get_dummies(XMod)
	
	customerApartment = X[:-1]
	X = X[-1:]
	
	print customerApartment
	print X
	
	model = GridSearchCV(GradientBoostingRegressor(), scoring='neg_mean_squared_error',
	                     param_grid={'loss' :('ls', 'huber'), 'learning_rate' : numpy.arange(0.05, 0.21, 0.05),
						 'n_estimators' : range(70, 111, 10), 'max_depth' : range(2, 4, 1)})
	#print dataset.head()
	#print dataset.tail()
	exit()			 
	model.fit(X, Y)
	
	print "!!!-.-.-!!!"
	#print model.cv_results_ #too long to print
	print model.best_estimator_
	print model.best_score_
	print model.best_params_
	#print model.best_index_ #not important
	print model.scorer_
	print model.n_splits_
	
		