import pymongo
import subprocess
import os

import DatabaseConfig

class Database(object):
	
	mongod = False
	
	def __init__(self):	
		self.mongoClient = False
		self.mongoDatabase = False
		self.mongoCollection = False
		print "Remember to use .Close() after you are finished using the database."
    
	def Open(self, conn):
		self.RunMongodIfOffline()
		if self.IsConnOpen():
			self.Close()
		self.CheckConnArgs(conn)
		
		self.mongoClient = pymongo.MongoClient(host=DatabaseConfig.host, port=DatabaseConfig.port)
		self.mongoDatabase = self.mongoClient[conn['database']]
		self.mongoCollection = self.mongoDatabase[conn['collection']]
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
			
	def InspectDatabase(self):
		self.RunMongodIfOffline()
		client = pymongo.MongoClient(host=DatabaseConfig.host, port=DatabaseConfig.port)
		
		databaseNames = client.database_names()
		
		for name in databaseNames:
			print 'Database ' + name + ':'
			database = client[name]
			collectionNames = database.collection_names()
			
			for name in collectionNames:
				print '----- Collection ' + name + ':'
				
				collection = database[name]
				print '     ----- Count documents: ',
				print collection.count()
				print '     ----- Document attributes: ',
				print collection.find_one().keys()
			print
				
		client.close()
		return True
		
	def Close(self):
		if self.IsConnOpen():
			self.mongoClient.close()
			self.mongoClient = False
			self.mongoDatabase = False
			self.mongoCollection = False
		self.TerminateMongod()
		return True
	
	def RunMongodIfOffline(self):
		if not self.IsMongodRunning():
			self.RunMongod()
		return True
			
	def RunMongod(self):
		if not self.IsMongodRunning():
			try:
				Database.mongod = subprocess.Popen([os.path.expanduser(DatabaseConfig.dbPath), "--dbpath", DatabaseConfig.dataPath], stdout=subprocess.PIPE)
			except:
				raise Exception("Couldn't start the database! Database path is:" + DatabaseConfig.dbPath + "Data path is:" + DatabaseConfig.dataPath)
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
							
	def TerminateMongod(self):
		if not self.IsMongodRunning():
			return True
		mongoShell = subprocess.Popen([os.path.expanduser(DatabaseConfig.mongoShellPath), DatabaseConfig.shellDatabase], stdin=subprocess.PIPE)
		mongoShell.communicate(DatabaseConfig.shellCloseMongodCommand)
		Database.mongod = False
		return True
		
	def IsMongodRunning(self, strict=False):
		if strict:
			client = pymongo.MongoClient(host=DatabaseConfig.host, port=DatabaseConfig.port, connectTimeoutMS=2000, serverSelectionTimeoutMS=3000)
			try:
				client.admin.command('ismaster')
				client.close()
				return True
			except:
				client.close()
				return False
		else:
			if Database.mongod:
				return True
			else:
				return False
			
	def IsConnOpen(self):
		if self.mongoClient:
			return True
		else:
			return False