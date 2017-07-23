from RealEstateValuationSystem.Database.Database import Database
from RealEstateValuationSystem.Database.DatabaseConfig import conn

class TestDatabase(object):
	def test_create_Database(self):
		db = Database()
		assert db.mongoClient == False
	
	def test_Open(self):
		db = Database()
		assert db.Open(conn) == True
		assert db.IsConnOpen() == True
		assert db.Close() == True
		
	def test_RunMongodIfOffline(self):
		db = Database()
		assert db.RunMongodIfOffline() == True
		assert db.Close() == True
		
	def test_RunMongod(self):
		db = Database()
		assert db.RunMongod() == True
		assert db.IsMongodRunning() == True
		assert db.Close() == True
		
	def test_CheckConnArgs(self):
		db = Database()
		assert db.CheckConnArgs(conn) == True
		
	def test_Close(self):
		db = Database()
		assert db.Close() == True
		assert db.IsMongodRunning() == False
		
	def test_IsMongodRunningF(self):
		db = Database()
		assert db.IsMongodRunning() == False
	
	def test_IsMongodRunningT(self):
		db = Database()
		assert db.RunMongod() == True
		assert db.IsMongodRunning() == True
		assert db.Close() == True
	
	def test_IsConnOpenF(self):
		db = Database()
		assert db.IsConnOpen() == False
		
	def test_IsConnOpenT(self):
		db = Database()
		assert db.Open(conn) == True
		assert db.IsConnOpen() == True
		assert db.Close() == True
		
	def test_TerminateMongod(self):
		db = Database()
		assert db.TerminateMongod() == True
		assert db.RunMongodIfOffline() == True
		assert db.IsMongodRunning() == True
		assert db.TerminateMongod() == True
		assert db.IsMongodRunning() == False
	
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
		
	def test_InspectDatabase(self):
		db = Database()
		assert db.InspectDatabase() == True
		assert db.Close() == True
		