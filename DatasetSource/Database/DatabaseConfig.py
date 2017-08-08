#Absolute path of mongod.exe
#Used by DatabaseController.py to start mongod.exe
dbPath = r"C:\Program Files\MongoDB\Server\3.2\bin\mongod.exe"
#Absolute path of where mongoDB stores the data
#Used by DatabaseController.py to locate the data
dataPath = r"C:\data\db"
#Absolute path of mongo.exe (mongo shell)
#Used by DatabaseController.py to correctly shutdown mongod.exe
mongoShellPath = r"C:\Program Files\MongoDB\Server\3.2\bin\mongo.exe"
#Hostname or IP address or Unix domain socket path of a single mongod
#Used by DatabaseController.py to connect to mongod.exe
host = r'localhost'
#Port number on which to connect
#Used by DatabaseController.py to connect to mongod.exe
port = 27017



