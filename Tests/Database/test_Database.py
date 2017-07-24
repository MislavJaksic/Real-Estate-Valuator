from RealEstateValuationSystem.Database.Database import Database
from RealEstateValuationSystem.Database.DatabaseConfig import conn

class TestDatabase(object):
	def test_template(self):
		pass
	
	def test_create_Database(self):
		db = Database()
		assert db.mongoClient == False
	
	def test_InspectDatabase(self):
		db = Database()
		assert db.InspectDatabase() == True
		assert db.Close() == True
		
	def test_Open(self):
		db = Database()
		assert db.Open(conn) == True
		assert db.IsConnOpen() == True
		assert db.Close() == True
		
	def test_CheckInputConn(self):
		db = Database()
		assert db.CheckInputConn(conn) == True
		
	def test_IsKeyInDictT(self):
		db = Database()
		dict = {'hello' : 55}
		assert db.IsKeyInDict('hello', dict) == True
		
	def test_IsKeyInDictF(self):
		db = Database()
		dict = {'hello' : 55}
		assert db.IsKeyInDict('hi', dict) == False
		
	def test_CheckInputTypeDictT(self):
		db = Database()
		dict = {}
		assert db.CheckInputTypeDict(dict) == True
		
	def test_CheckInputTypeDictF(self):
		db = Database()
		number = 7
		assert db.CheckInputTypeDict(number) == False
		
	def test_IsParamasInDatabaseT(self):
		db = Database()
		db.RunMongod()
		assert db.IsParamasInDatabase(conn['database'], conn['collection']) == True
		db.Close()
		
	def test_RunMongodIfOffline(self):
		db = Database()
		assert db.RunMongodIfOffline() == True
		assert db.Close() == True
		
	def test_RunMongod(self):
		db = Database()
		assert db.RunMongod() == True
		assert db.IsMongodRunning() == True
		assert db.Close() == True
		
	def test_Close(self):
		db = Database()
		assert db.Close() == True
		assert db.IsMongodRunning() == False
		
	def test_ShutdownMongod(self):
		db = Database()
		assert db.ShutdownMongod() == True
		assert db.RunMongodIfOffline() == True
		assert db.IsMongodRunning() == True
		assert db.ShutdownMongod() == True
		assert db.IsMongodRunning() == False
		
	def test_IsMongodRunningT(self):
		db = Database()
		assert db.RunMongod() == True
		assert db.IsMongodRunning() == True
		assert db.Close() == True
	
	def test_IsMongodRunningF(self):
		db = Database()
		assert db.IsMongodRunning() == False
	
	def test_IsConnOpenF(self):
		db = Database()
		assert db.IsConnOpen() == False
		
	def test_IsConnOpenT(self):
		db = Database()
		assert db.Open(conn) == True
		assert db.IsConnOpen() == True
		assert db.Close() == True
	
	def test_GetDataIterF(self):
		db = Database()
		cond = {}
		iter = db.GetDataIter(cond)
		assert iter == False
		assert db.Close() == True
		
	def test_GetDataIterT(self):
		db = Database()
		assert db.Open(conn) == True
		cond = {}
		iter = db.GetDataIter(cond)
		assert iter != False
		assert db.Close() == True
		
	
		