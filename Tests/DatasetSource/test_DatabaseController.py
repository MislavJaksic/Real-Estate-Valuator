from RealEstateValuationSystem.DatasetSource.Database.DatabaseController import DatabaseControllerManager, DatabaseController
import pytest
conn = {'database' : 'test', 'collection' : 'restaurants'}

class TestDatabaseOn(object):
  @pytest.fixture(scope='class')
  def db(self):
    with DatabaseControllerManager() as database:
      yield database
    
  def test_Inspect(self, db):
    assert db.Inspect() == True
    
  def test_Open(self, db):
    assert db.Open(conn) == True
    db._CloseCollection()
  
  def test_IsCollectionInDatabaseT(self, db):
    assert db._IsCollectionInDatabase(conn) == True
    
  def test_IsCollectionInDatabaseF(self, db): #take an infinite amount of time after the test passes (solved by marking sure there is only a single MongoClient)
    wrongConn = {'database' : 'test', 'collection' : 'wrong'}
    assert db._IsCollectionInDatabase(wrongConn) == False
    
  def test_IsMongodRunningT(self, db):
    assert db._IsMongodRunning() == True
    
  def test_IsCanConnectT(self, db):
    assert db._IsCanConnect() == True
    
  def test_FindT(self, db):
    cond = {}
    db.Open(conn)
    assert db.Find(cond) != []
    db._CloseCollection()
    
  def test_FindF(self, db):
    cond = {}
    assert db.Find(cond) == []
    
  def test_FindDistinctT(self, db):
    cond = {}
    db.Open(conn)
    assert db.FindDistinct(cond, u'name') != []
    db._CloseCollection()
    
  def test_FindDistinctF(self, db):
    cond = {}
    assert db.FindDistinct(cond, u'placeholder') == []
    
  # def test_Insert(self, db):
    # pass
    
  def test_IsCollectionOpenT(self, db):
    db.Open(conn)
    assert db._IsCollectionOpen() == True
    db._CloseCollection()
    
  def test_IsCollectionOpenF(self, db):
    db._CloseCollection()
    assert db._IsCollectionOpen() == False
    
class TestDatabaseOff(object):
  @pytest.fixture(scope='class')
  def db(self):
    database = DatabaseController()
    yield database
      
  def test_IsCollectionPathT(self, db): 
    assert db._IsCollectionPath(conn) == True
    
  def test_IsCollectionPathF(self, db):
    notColl = []
    with pytest.raises(Exception) as e_info:
      db._IsCollectionPath(notColl)
      
  def test_IsKeyInDictT(self, db):
    dict = {'hello' : 55}
    assert db._IsKeyInDict('hello', dict) == True
    
  def test_IsKeyInDictF(self, db):
    dict = {'hello' : 55}
    assert db._IsKeyInDict('hi', dict) == False
    
  def test_IsCollectionInDatabaseE(self, db):
    with pytest.raises(Exception) as e_info:
      db._IsCollectionInDatabase('some', 'thing')
      
  def test_CloseCollection(self, db):
    assert db._CloseCollection() == True
    
  def test_StopMongod(self, db):
    assert db._StopMongod() == True
    
  def test_IsMongodRunningF(self, db):
    assert db._IsMongodRunning() == False
    
  def test_IsCanConnectF(self, db):
    assert db._IsCanConnect() == False
    