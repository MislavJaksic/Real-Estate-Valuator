#Absolute path of mongod.exe
#Used by Database.py to start mongod.exe
dbPath = r"C:\Program Files\MongoDB\Server\3.2\bin\mongod.exe"
#Absolute path of where mongoDB stores the data
#Used by Database.py to locate the data
dataPath = r"C:\data\db"
#Absolute path of mongo.exe (mongo shell)
#Used by Database.py to correctly shutdown mongod.exe
mongoShellPath = r"C:\Program Files\MongoDB\Server\3.2\bin\mongo.exe"
#Hostname or IP address or Unix domain socket path of a single mongod
#Used by Database.py to connect to mongod.exe
host = r'localhost'
#Port number on which to connect
#Used by Database.py to connect to mongod.exe
port = 27017

#-.-.-.-.- #Constants #-.-.-.-.-
#Name of the database to which the shell will login
#Used by Database.py to give mongo shell the ability to execute the shutdown command
shellDatabase = r'admin'
#Mongo shell shutdown command
#Used by Database.py to correctly shutdown mongod.exe
shellCloseMongodCommand = r'db.shutdownServer()'



