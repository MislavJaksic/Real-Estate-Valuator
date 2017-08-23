import sys
import os
sys.path.insert(0, os.path.abspath('../..'))

from RealEstateValuationSystem.DatasetAnalysis.ApartmentForSaleCollection import DatasetConfig
from RealEstateValuationSystem.DatasetTransformation.DatasetTransformer import DatasetTransformer
from RealEstateValuationSystem.DatasetSource import DatasetLoader
from RealEstateValuationSystem.DatasetTransformation import TransformationScripts

from sklearn.linear_model import LinearRegression, ElasticNet, ElasticNetCV
from sklearn.model_selection import GridSearchCV
from sklearn.feature_selection import SelectKBest, f_regression, RFECV
from sklearn.ensemble import GradientBoostingRegressor
import numpy
import pandas

placeThreshold = 200
townThreshold = 200

def PredictApartmentValue(customerApartment):
	adApartments = LoadApartmentsInTheSameLocation(customerApartment)
	if adApartments.empty:
		return -1
	apartments = JoinCustomerAndAdApartments(customerApartment, adApartments)
	transformer = TransformApartments(apartments)
	X, Y, customerApartment = SplitDepAndIndepColumns(transformer)
	
	model = GridSearchCV(GradientBoostingRegressor(), scoring='neg_mean_squared_error',
	                     param_grid={'loss' :('ls', 'huber'), 'learning_rate' : numpy.arange(0.05, 0.21, 0.05),
						 'n_estimators' : range(70, 111, 10), 'max_depth' : range(2, 4, 1)})
	
	model.fit(X, Y)
	print "Predicted interval value:"
	print model.predict(customerApartment)
	print "!!!-.-.-!!!"
	#print model.cv_results_ #too long to print
	print model.best_estimator_
	print model.best_score_
	print model.best_params_
	#print model.best_index_ #not important
	print model.scorer_
	print model.n_splits_
	
	price = model.predict(customerApartment)[0]
	price = numpy.expm1(price)
	price = int(price)
	return price
	
def LoadApartmentsInTheSameLocation(customerApartment):
	apartments = DatasetLoader.Load(DatasetConfig.conn, {'place' : customerApartment['place'][0]})
	count = apartments['place'].count()
	if count < placeThreshold:
		apartments = DatasetLoader.Load(DatasetConfig.conn, {'town' : customerApartment['town'][0]})
		count = apartments['town'].count()
		if count < townThreshold:
			return pandas.DataFrame()
	return apartments
	
def JoinCustomerAndAdApartments(customerApartment, adApartments):
	customerApartment['priceInEuros'] = [100000]
	customerApartment['sellerLink'] = [u'/korisnik/']
	customerApartment = pandas.DataFrame(customerApartment)
	
	apartments = pandas.concat([adApartments, customerApartment], ignore_index=True)
	return apartments

def TransformApartments(apartments):
	transformer = DatasetTransformer(apartments)
	transformer.DropColumns(DatasetConfig.dropColumns)
	
	TransformationScripts.MakeTransformationsForApartmentForSaleCollection(transformer)
	return transformer

def SplitDepAndIndepColumns(transformer):
	Y = transformer.dataset['priceInEuros']
	transformer.DropColumns(['priceInEuros'])
	X = transformer.dataset
	
	customerApartment = X[-1:]
	X = X[:-1]
	Y = Y[:-1]
	return X, Y, customerApartment
	