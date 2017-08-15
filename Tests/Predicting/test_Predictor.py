from RealEstateValuationSystem.Predicting import Predictor

FplaceFTown = {'town': [u'Brezovica'], 'numberOfParkingSpaces': [0], 'floor': [1], 'state': [u'Grad Zagreb'],
            'place': [u'Brezovica'], 'size': [80]}
TplaceTTown = {'town': [u'Donji Grad'], 'numberOfParkingSpaces': [1], 'floor': [7], 'state': [u'Grad Zagreb'],
            'place': [u'Donji grad'], 'size': [30]}
FplaceTTown = {'town': [u'Pe\u0161\u010denica - \u017ditnjak'], 'numberOfParkingSpaces': [0], 'floor': [u'Potkrovlje'], 'state': [u'Grad Zagreb'],
			   'place': [u'Feren\u0161\u010dica'], 'size': [50]}

# def test_PredictApartmentValue():
	# assert Predictor.PredictApartmentValue(FplaceFTown) == True
	
# def test_LoadApartmentsInTheSameLocationFF():
	# assert Predictor.LoadApartmentsInTheSameLocation(FplaceFTown) == []
	
# def test_LoadApartmentsInTheSameLocationTT():
	# apartments = Predictor.LoadApartmentsInTheSameLocation(TplaceTTown)
	# assert apartments['place'][0] == 'Donji grad'
	
# def test_LoadApartmentsInTheSameLocationFT():
	# apartments = Predictor.LoadApartmentsInTheSameLocation(FplaceTTown)
	# assert apartments['town'][0] == u'Pe\u0161\u010denica - \u017ditnjak'
	
# def test_JoinCustomerAndAdApartmentsTT():
	# adApartments = Predictor.LoadApartmentsInTheSameLocation(TplaceTTown)
	# apartments = Predictor.JoinCustomerAndAdApartments(TplaceTTown, adApartments)
	# assert apartments['place'][0] == 'Donji grad'
	
# def test_JoinCustomerAndAdApartmentsFT():
	# adApartments = Predictor.LoadApartmentsInTheSameLocation(FplaceTTown)
	# apartments = Predictor.JoinCustomerAndAdApartments(FplaceTTown, adApartments)
	# assert apartments['town'][0] == u'Pe\u0161\u010denica - \u017ditnjak'
	
# def test_TransformApartments():
	# adApartments = Predictor.LoadApartmentsInTheSameLocation(FplaceTTown)
	# apartments = Predictor.JoinCustomerAndAdApartments(FplaceTTown, adApartments)
	# transformer = Predictor.TransformApartments(apartments)
	# assert transformer.dataset['sellerLink'][0] == 2
	
# def test_SplitDepAndIndepColumns():
	# adApartments = Predictor.LoadApartmentsInTheSameLocation(FplaceTTown)
	# apartments = Predictor.JoinCustomerAndAdApartments(FplaceTTown, adApartments)
	# transformer = Predictor.TransformApartments(apartments)
	# X, Y, customerApartment = Predictor.SplitDepAndIndepColumns(transformer)
	# assert customerApartment['sellerLink'][262] == 1
	
def test_PredictApartmentValue():
	value = Predictor.PredictApartmentValue(FplaceTTown)
	assert ((value > 11.0) and (value < 11.2)) == True
		