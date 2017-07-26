import sys
import os
sys.path.insert(0, os.path.abspath('../..'))

from RealEstateValuationSystem.InputControl.InputController import InputController

import pymongo
import subprocess
import os

import DatabaseConfig

class Database(object):
	"""Data Access Object controls access to the database. Uses pymongo to access MongoDB.
	Attributes: mongod is a process where the database is running.
	            mongoClient, mongoDatabase, mongoCollection store information to which collection the user
				is connected."""
	mongod = False
	
	def __init__(self):	
		self.mongoClient = False
		self.mongoDatabase = False
		self.mongoCollection = False
		print "Remember to use .Close() after you are finished using the database."
    
	def InspectDatabase(self):
		"""Turnspython on the database. Writes out the names of all databases, collections and document attributes
		as well as the number of documents in a collection. Always returns True."""
		self.RunMongodIfOffline()
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
		"""Turns on the database. Opens a connection to a MongoDB collection. Always returns True."""
		self.CheckInputConn(conn)
		
		self.RunMongodIfOffline()
		if self.IsConnOpen():
			self.Close()
		
		self.mongoClient = pymongo.MongoClient(host=DatabaseConfig.host, port=DatabaseConfig.port)
		self.mongoDatabase = self.mongoClient[conn['database']]
		self.mongoCollection = self.mongoDatabase[conn['collection']]
		return True
	
	def CheckInputConn(self, conn):
		"""Checks if the input is correct. Closes the database and raises an exception if the input is
		rejected, otherwise returns True."""
		if not InputController.IsDict(conn):
			self.Close()
			raise Exception("Cannot open connection because the paramater is not a dictionary")
		if not self.IsKeyInDict('database', conn):
			self.Close()
			raise Exception("Cannot open connection because the database name is missing")
		if not self.IsKeyInDict('collection', conn):
			self.Close()
			raise Exception("Cannot open connection because the collection name is missing")

		if self.IsMongodRunning():
			self.IsParamasInDatabase(conn['database'], conn['collection'])
		return True
	
	def IsKeyInDict(self, key, dict):
		"""Checks if the key is in the dictionary. If it is, returns True, if not, returns False."""
		exists = dict.get(key)
		if exists == None:
			return False
		return True
		
	def IsParamasInDatabase(self, dbName, collName):
		"""Checks if the database and collection names are in the database. Closes the database and
		raises an exception if the input is rejected, otherwise returns True."""
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
	
	def RunMongodIfOffline(self):
		"""A helper function."""
		if not self.IsMongodRunning():
			self.RunMongod()
		return True
		
	def RunMongod(self):
		"""Run mongo database process called mongod. If it cannot be run, raises an exception, otherwise
		return True."""
		if not self.IsMongodRunning():
			try:
				Database.mongod = subprocess.Popen([os.path.expanduser(DatabaseConfig.dbPath), "--dbpath", DatabaseConfig.dataPath], stdout=subprocess.PIPE)
			except:
				raise Exception("Couldn't start the database! Database path is:" + DatabaseConfig.dbPath + "Data path is:" + DatabaseConfig.dataPath)
		return True
		
	def Close(self):
		"""Close the currect connection to the database if there is any and gently shuts down the mongoDB
		process mongod. Always returns True."""
		if self.IsConnOpen():
			self.mongoClient.close()
			self.mongoClient = False
			self.mongoDatabase = False
			self.mongoCollection = False
		self.ShutdownMongod()
		return True
		
	def ShutdownMongod(self):
		"""Closes the mongoDB process gently using mongo shell commands if there is something to shut down.
		Always returns True."""
		if not self.IsMongodRunning():
			return True
		mongoShell = subprocess.Popen([os.path.expanduser(DatabaseConfig.mongoShellPath), DatabaseConfig.shellDatabase], stdin=subprocess.PIPE)
		mongoShell.communicate(DatabaseConfig.shellCloseMongodCommand)
		Database.mongod = False
		return True
		
	def IsMongodRunning(self, strict=False):
		"""Checks input. Checks if the database is running. Passing strict=True makes the function attempt
		to connect to the database. Returns True if the database is running, False if not."""
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
		"""Return a data iterator which fetches documents from a collection which satisfy the condition.
		Documents have the follow the pattern: {u'key1' : [u'value1'], u'key2' : [value2], ...}.
		If distinct=True it fetches unique documents. Returns the iterator or False if the connection
		is close or if an error occured."""
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
		"""Store a new document into the database collection. Returns True if the document was stored
		or False if the connection is close or if an error occured."""
		if self.IsConnOpen():
			try:
				self.mongoCollection.insert(entry)
				return True
			except:
				return False
		else:
			return False
			
	def IsConnOpen(self):
		"""Checks if the connection to a collection is open. If it is, returns True, otherwise it return False."""
		if self.mongoClient:
			return True
		else:
			return False
			