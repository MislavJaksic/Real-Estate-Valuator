import sys
import os
sys.path.insert(0, os.path.abspath('../..'))

from RealEstateValuationSystem.InputControl.InputController import InputController
import DatabaseConfig

import pymongo
import subprocess
import os



class Database(object):
	"""Data Access Object. Uses pymongo to access MongoDB. Controls the mongod.exe process.
	Attributes: mongod is a process in which mongod.exe is running.
	            mongoClient, mongoDatabase, mongoCollection store information about the collection
				to which the user is connected."""
	mongod = False
	
	def __init__(self):	
		self.mongoClient = False
		self.mongoDatabase = False
		self.mongoCollection = False
		print "Remember to use .Close() after you done using the database."
    
	def InspectDatabase(self):
		"""Writes out the names of all mongo databases, collections, documents' attributes
		and documents count. Always returns True."""
		self.RunMongod()
		client = pymongo.MongoClient(host=DatabaseConfig.host, port=DatabaseConfig.port)
		
		databaseNames = client.database_names()
		for name in databaseNames:
			print '\'database\' : ' + name
			database = client[name]
			
			collectionNames = database.collection_names()
			for name in collectionNames:
				print '----- \'collection\' : ' + name
				
				collection = database[name]
				print '     ----- Count documents: ',
				print collection.count()
				print '     ----- Document attributes: ',
				print collection.find_one().keys()
			print
				
		client.close()
		return True
		
	def Open(self, conn):
		"""Opens a new connection to a mongo collection. Always returns True."""
		self.CheckInputConn(conn)
		
		self.RunMongod()
		if self.IsConnOpen():
			self.Close()
		
		self.mongoClient = pymongo.MongoClient(host=DatabaseConfig.host, port=DatabaseConfig.port)
		self.mongoDatabase = self.mongoClient[conn['database']]
		self.mongoCollection = self.mongoDatabase[conn['collection']]
		return True
	
	def CheckInputConn(self, conn):
		"""Returns True if a Python dictionary follows the pattern {'database':'dbName', 'collection':'collName'},
		otherwise closes the database and raises an exception."""
		if not InputController.IsDict(conn):
			self.Close()
			raise Exception("Cannot open connection because the paramater is not a dictionary.")
		if not self.IsKeyInDict('database', conn):
			self.Close()
			raise Exception("Cannot open connection because the 'database' name is missing.")
		if not self.IsKeyInDict('collection', conn):
			self.Close()
			raise Exception("Cannot open connection because the 'collection' name is missing.")

		if self.IsMongodRunning():
			self.IsParamsInDatabase(conn['database'], conn['collection'])
		return True
	
	def IsKeyInDict(self, key, dict):
		"""If it is, returns True, if not, returns False."""
		exists = dict.get(key)
		if exists == None:
			return False
		return True
		
	def IsParamsInDatabase(self, dbName, collName):
		"""If mongo database and collection names are in the database, returns True, otherwise closes
		the database and raises an exception."""
		client = pymongo.MongoClient()
		if not dbName in client.database_names():
			self.Close()
			raise Exception("Database name " + dbName + " doesnt exist in the client")
		
		database = client[dbName]
		if not collName in database.collection_names():
			self.Close()
			raise Exception("Collection name " + collName + " doesnt exist in the client")
		
		client.close()
		return True
		
	def RunMongod(self):
		"""Runs database if it isn't running already. If it cannot be run, raises an exception, otherwise
		return True."""
		if not self.IsMongodRunning():
			try:
				Database.mongod = subprocess.Popen([os.path.expanduser(DatabaseConfig.dbPath), "--dbpath", DatabaseConfig.dataPath], stdout=subprocess.PIPE)
			except:
				raise Exception("Couldn't start the database! Database path is:" + DatabaseConfig.dbPath + "Data path is:" + DatabaseConfig.dataPath)
		return True
		
	def Close(self):
		"""Closes an open connection and closes the database. Always returns True."""
		if self.IsConnOpen():
			self.mongoClient.close()
			self.mongoClient = False
			self.mongoDatabase = False
			self.mongoCollection = False
		self.ShutdownMongod()
		return True
		
	def ShutdownMongod(self):
		"""Closes the database. Always returns True."""
		if not self.IsMongodRunning():
			return True
		mongoShell = subprocess.Popen([os.path.expanduser(DatabaseConfig.mongoShellPath), DatabaseConfig.shellDatabase], stdin=subprocess.PIPE)
		mongoShell.communicate(DatabaseConfig.shellCloseMongodCommand)
		Database.mongod = False
		return True
		
	def IsMongodRunning(self, strict=False):
		"""Returns True if the database is running, False if not. If strict=True it will
		try to connect to the database instead of just checking the class attribute."""
		if not InputController.IsBool(strict):
			self.Close()
			raise Exception("Strict is not a boolean value")
			
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
		
	def GetDataIter(self, condition, distinct=False):
		"""Return a data iterator which fetches documents from a mongo collection which satisfy the condition.
		Fetched documents follow the pattern {u'key1' : [u'value1'], u'key2' : [value2], ...}.
		If distinct=True it fetches unique documents. Returns the iterator or False if the connection
		is closed or if an error occured."""
		if not InputController.IsBool(distinct):
			self.Close()
			raise Exception("Distinct is not a boolean value")
		if self.IsConnOpen():
				try:
					if distinct:
						return self.mongoCollection.find(condition).distinct(distinct)
					else:
						return self.mongoCollection.find(condition)
				except:
					print "Cannot execute .find() in mongoDB"
					return False
		else:
			print "Connection is closed."
			return False
	
	def Store(self, entry):
		"""Store a new document into the database mongo collection. Returns True if the document was stored
		or False if the connection is closed or if an error occured."""
		if self.IsConnOpen():
			try:
				self.mongoCollection.insert(entry)
				return True
			except:
				return False
		else:
			return False
			
	def IsConnOpen(self):
		"""Checks if the connection to a mongo collection is open. If it is, returns True,
		otherwise it return False."""
		if self.mongoClient:
			return True
		else:
			return False
			