from RealEstateValuationSystem.DatasetSource.Database.DatabaseController import DatabaseController
conn = {'database' : 'test', 'collection' : 'restaurants'}

class TestDatabase(object):
	def test_create_Database(self):
		db = DatabaseController()
		assert db.mongoClient == False
	
	def test_InspectDatabase(self):
		db = DatabaseController()
		assert db.InspectDatabase() == True
		assert db.Close() == True
		
	def test_Open(self):
		db = DatabaseController()
		assert db.Open(conn) == True
		assert db.IsConnOpen() == True
		assert db.Close() == True
		
	def test_CheckInputConn(self):
		db = DatabaseController()
		assert db.CheckInputConn(conn) == True
		
	def test_IsKeyInDictT(self):
		db = DatabaseController()
		dict = {'hello' : 55}
		assert db.IsKeyInDict('hello', dict) == True
		
	def test_IsKeyInDictF(self):
		db = DatabaseController()
		dict = {'hello' : 55}
		assert db.IsKeyInDict('hi', dict) == False
		
	def test_IsParamsInDatabaseT(self):
		db = DatabaseController()
		db.RunMongod()
		assert db.IsParamsInDatabase(conn['database'], conn['collection']) == True
		db.Close()
		
	def test_RunMongod(self):
		db = DatabaseController()
		assert db.RunMongod() == True
		assert db.IsMongodRunning() == True
		assert db.Close() == True
		
	def test_Close(self):
		db = DatabaseController()
		assert db.Close() == True
		assert db.IsMongodRunning() == False
		
	def test_ShutdownMongod(self):
		db = DatabaseController()
		assert db.ShutdownMongod() == True
		assert db.RunMongod() == True
		assert db.IsMongodRunning() == True
		assert db.ShutdownMongod() == True
		assert db.IsMongodRunning() == False
		
	def test_IsMongodRunningT(self):
		db = DatabaseController()
		assert db.RunMongod() == True
		assert db.IsMongodRunning() == True
		assert db.Close() == True
	
	def test_IsMongodRunningF(self):
		db = DatabaseController()
		assert db.IsMongodRunning() == False
	
	def test_IsConnOpenF(self):
		db = DatabaseController()
		assert db.IsConnOpen() == False
		
	def test_IsConnOpenT(self):
		db = DatabaseController()
		assert db.Open(conn) == True
		assert db.IsConnOpen() == True
		assert db.Close() == True
	
	def test_GetDataIterF(self):
		db = DatabaseController()
		cond = {}
		iter = db.GetDataIter(cond)
		assert iter == False
		assert db.Close() == True
		
	def test_GetDataIterT(self):
		db = DatabaseController()
		assert db.Open(conn) == True
		cond = {}
		iter = db.GetDataIter(cond)
		assert iter != False
		assert db.Close() == True
		
	
		
