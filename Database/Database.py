import pymongo
import subprocess
import os

import DatabaseConfig

class Database(object):
	
	mongod = None
	
	def __init__(self):	
		self.mongoClient = None
		self.mongoDatabase = None
		self.mongoCollection = None
    
	def Open(self, conn):
		self.RunMongodIfOffline()
		if self.IsConnOpen():
			self.Close()
		self.CheckConnArgs(conn)
		
		self.mongoClient = pymongo.MongoClient()
		self.mongoDatabase = self.mongoClient[conn['database']]
		self.mongoCollection = self.mongoDatabase[conn['collection']]
		return True
	
	def RunMongodIfOffline(self):
		if not self.IsMongodRunning():
			self.RunMongod()
		return True
			
	def RunMongod(self):
		if not self.IsMongodRunning():
			try:
				Database.mongod = subprocess.Popen([os.path.expanduser(DatabaseConfig.dbPath), "--dbpath", DatabaseConfig.dataPath])
			except:
				raise Exception("Couldn't start the database! Database path is:" + dbPath + "Data path is:" + dataPath)
		return True
	
	def CheckConnArgs(self, conn):
		dbArgExists = conn.get('database')
		if dbArgExists == None:
			dbArgExists = "None"
		collArgExists = conn.get('collection')
		if collArgExists == None:
			collArgExists = "None"
			
		if dbArgExists == "None" or collArgExists == "None":
			self.Close()
			raise Exception("Cannot open connection because an argument is missing" + "Database arg:" + dbArgExists + "Collection arg:" + collArgExists)
		
		if self.IsMongodRunning():
			client = pymongo.MongoClient()
			if not dbArgExists in client.database_names():
				self.Close()
				raise Exception("Database name doesnt exist in the client" + "Database arg:" + dbArgExists)
			
			database = client[dbArgExists]
			if not collArgExists in database.collection_names():
				self.Close()
				raise Exception("Collection name doesnt exist in the client" + "Collection arg:" + collArgExists)
			
			client.close()
		return True
			
	def Close(self):
		if self.IsConnOpen():
			self.mongoClient.close()
			self.mongoClient = None
			self.mongoDatabase = None
			self.mongoCollection = None
		self.TerminateMongod()
		return True
				
	def TerminateMongod(self):
		if not self.IsMongodRunning():
			return True
		Database.mongod.terminate()
		Database.mongod = None
		return True
		
	def IsMongodRunning(self):
		if Database.mongod == None:
			return False
		else:
			return True

	def GetDataIter(self, condition, distinct=False):
		if self.IsConnOpen():
				try:
					if distinct:
						return self.mongoCollection.find(condition).distinct(distinct)
					else:
						return self.mongoCollection.find(condition)
				except:
					return False
		else:
			return False
	
	def Store(self, entry):
		if self.IsConnOpen():
			try:
				self.mongoCollection.insert(entry)
				return True
			except:
				return False
		else:
			return False
			
	def IsConnOpen(self):
		if self.mongoClient == None:
			return False
		else:
			return True