from RealEstateValuationSystem.Database.Database import Database
from RealEstateValuationSystem.Database.DatabaseConfig import conn

class TestDatabase(object):
	def test_create_Database(self):
		db = Database()
		assert db.mongoClient == None
		assert Database.mongod == None
	
	def test_Open(self):
		db = Database()
		assert db.Open(conn) == True
		assert db.mongoCollection != None
		assert db.Close() == True
		assert Database.mongod == None
		
	def test_RunMongodIfOffline(self):
		db = Database()
		assert db.RunMongodIfOffline() == True
		assert db.Close() == True
		assert Database.mongod == None
		
	def test_RunMongod(self):
		db = Database()
		assert db.RunMongod() == True
		assert Database.mongod != None
		assert db.Close() == True
		assert Database.mongod == None
		
	def test_CheckConnArgs(self):
		db = Database()
		assert db.CheckConnArgs(conn) == True
		assert Database.mongod == None
		
	def test_Close(self):
		db = Database()
		assert db.Close() == True
		assert Database.mongod == None
		
	def test_IsMongodRunningF(self):
		db = Database()
		assert db.IsMongodRunning() == False
		assert Database.mongod == None
	
	def test_IsMongodRunningT(self):
		db = Database()
		assert db.RunMongod() == True
		assert db.IsMongodRunning() == True
		assert db.Close() == True
		assert Database.mongod == None
	
	def test_IsConnOpenF(self):
		db = Database()
		assert db.IsConnOpen() == False
		assert Database.mongod == None
		
	def test_IsConnOpenT(self):
		db = Database()
		assert db.Open(conn) == True
		assert db.IsConnOpen() == True
		assert db.Close() == True
		assert Database.mongod == None
		
	def test_TerminateMongod(self):
		db = Database()
		assert db.TerminateMongod() == True
		assert Database.mongod == None
	
	def test_GetDataIterF(self):
		db = Database()
		cond = {}
		iter = db.GetDataIter(cond)
		assert iter == False
		assert db.Close() == True
		assert Database.mongod == None
		
	def test_GetDataIterT(self):
		db = Database()
		assert db.Open(conn) == True
		cond = {}
		iter = db.GetDataIter(cond)
		assert iter != False
		assert db.Close() == True
		assert Database.mongod == None
		
		
		