#Where mongo.exe is installed
#Pass starts mongod
dbPath = r"C:\Program Files\MongoDB\Server\3.2\bin\mongod.exe"
#Where database data is stored
#Pass it to mongo.exe as an argument of --dbpath
dataPath = r"C:\data\db"

conn = {'database':'NjuskaloRealEstateAds', 'collection':'ApartmentForSaleCollection'}