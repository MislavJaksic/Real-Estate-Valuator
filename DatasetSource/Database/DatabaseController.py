import sys
import os
sys.path.insert(0, os.path.abspath('../../..'))

from RealEstateValuationSystem.InputControl.InputController import InputController
import DatabaseConfig

import pymongo
import subprocess
import os


class DatabaseController(object):
    """Data Access Object.
    Attributes: mongod stores a mongod.exe process. There can be only one.
                mongoClient stores an entry point to the database. There can be only one."""
    mongod = False
    mongoClient = pymongo.MongoClient(host=DatabaseConfig.host, port=DatabaseConfig.port, connectTimeoutMS=2500, serverSelectionTimeoutMS=3000)
    
    def __init__(self):
        self.mongoDatabase = False
        self.mongoCollection = False
    
    def RunMongod(self):
      """Run mongod if it isn't already running."""
      if not self._IsMongodRunning():
        try:
          DatabaseController.mongod = subprocess.Popen([os.path.expanduser(DatabaseConfig.dbPath), "--dbpath", DatabaseConfig.dataPath],
                                                        stdout=subprocess.PIPE)
        except:
          self.CloseAndStop()
          raise Exception("Couldn't start the database! DatabaseConfig database path is:" + DatabaseConfig.dbPath + "DatabaseConfig data path is:" + DatabaseConfig.dataPath)
      return True
        
    def Inspect(self):
      """Write out the names of all mongo databases, collections, document attributes and count."""
      databaseNames = DatabaseController.mongoClient.database_names()
      for name in databaseNames:
        print '\'database\' : ' + name
        database = DatabaseController.mongoClient[name]
        collectionNames = database.collection_names()
        for name in collectionNames:
          print '----- \'collection\' : ' + name
          collection = database[name]
          print '     ----- Count documents: ',
          print collection.count()
          print '     ----- Document attributes: ',
          print collection.find_one().keys()
        print
              
      return True
        
    def Open(self, coll):
      """Open a mongo collection."""
      self._IsCollectionPath(coll)
      
      self._CloseCollection()
      
      self.mongoDatabase = DatabaseController.mongoClient[coll['database']]
      self.mongoCollection = self.mongoDatabase[coll['collection']]
      return True
        
    def _IsCollectionPath(self, coll):
      """Is a collection if {'database':'dbName', 'collection':'collName'}."""
      if not InputController.IsDict(coll):
          self.CloseAndStop()
          raise Exception("Argument has to be a dictionary of pattern {'database':'dbName', 'collection':'collName'}")
      if not self._IsKeyInDict('database', coll):
          self.CloseAndStop()
          raise Exception("No key 'database'")
      if not self._IsKeyInDict('collection', coll):
          self.CloseAndStop()
          raise Exception("No key 'collection'")
      return True
        
    def _IsKeyInDict(self, key, dict):
      """Key is in dict if a value can be extracted."""
      exists = dict.get(key)
      if exists == None:
          return False
      return True
        
    def Find(self, condition):
      """Return a document iterator where documents are structures as
      {u'key1' : [u'value1'], u'key2' : [value2], ...}. Condition is structured as
      {'size' : {'$lt' : 500}}, {'priceInEuros' : {'$gt' : 5000}}."""
      if self._IsCollectionOpen():
          return self.mongoCollection.find(condition)
      else:
        return []
            
    def FindDistinct(self, condition, column):
      """Return a list of unique values in a column. Condition is structured as
      {'size' : {'$lt' : 500}}, {'priceInEuros' : {'$gt' : 5000}}."""
      if self._IsCollectionOpen():
        return self.mongoCollection.find(condition).distinct(column)
      else:
        return []
            
    def Insert(self, entry):
      """Insert a new document into the open collection."""
      if self._IsCollectionOpen():
        try:
          self.mongoCollection.insert(entry)
          return True
        except:
          print "Pymongo cannot execute .insert()."
          return False
      else:
        print "Connection is closed."
        return False
      
    def CloseAndStop(self):
      """Closes an open connection and closes the database."""
      self._CloseCollection()
      self._StopMongod()
      return True
        
    def _CloseCollection(self):
      """Close a collection if it is open."""
      if self._IsCollectionOpen():
        self.mongoDatabase = False
        self.mongoCollection = False
      return True
    
    def _IsCollectionOpen(self):
      """Check if a collection is open."""
      if self.mongoCollection:
        return True
      else:
        return False
            
    def _StopMongod(self):
      """Close the database."""
      if not self._IsMongodRunning():
        return True
      mongoShell = subprocess.Popen([os.path.expanduser(DatabaseConfig.mongoShellPath), r'admin'],
                                     stdin=subprocess.PIPE)
      mongoShell.communicate(r'db.shutdownServer()')
      DatabaseController.mongod = False
      return True
        
    def _IsMongodRunning(self):
      """Has mongod been spawned by DatabaseController."""
      if DatabaseController.mongod:
        return True
      else:
        return False
    
    def _IsCollectionInDatabase(self, coll):
      """Return True if the collection is in the database."""
      if not self._IsCollectionPath(coll):
        return False
      
      dbName = coll['database']
      collName = coll['collection']
      if dbName in DatabaseController.mongoClient.database_names():
        database = DatabaseController.mongoClient[dbName]
        if collName in database.collection_names():
          return True
      return False
        
    def _IsCanConnect(self):
      """Attempt to connect to a database."""
      try:
        DatabaseController.mongoClient.admin.command('ismaster')
        return True
      except:
        return False
            
class DatabaseControllerManager(object):
  
  def __enter__(self):
    self.db = DatabaseController()
    self.db.RunMongod()
    return self.db
    
  def __exit__(self, exc_type, exc_value, traceback):
    self.db.CloseAndStop()
    