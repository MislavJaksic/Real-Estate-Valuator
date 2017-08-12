## Database

MongoDB is the database that the system currently uses. MongoDB is accessed through DatabaseController which
in turn uses Pymongo, a database driver.

### DatabaseController

Responsibilities: .RunMongod() creates a MongoDB instance, .Inspect() displays the contents of the database,
.Open() opens a connection to a collection, .Find() returns documents from an open collection, .FindDistinct()
returns distinct values from an open collection, .Insert() inserts documents into an open collection,
.CloseAndStop() closes the MongoDB instance "gently" to make it release it's locks and save data. The class
makes sure there is only one MongoDB instance running at any time. The class makes sure there is only one
MongoClient as per [this recommendation](https://api.mongodb.com/python/current/faq.html#how-does-connection-pooling-work-in-pymongo).

It is up to the user to use .CloseAndStop() to close the MongoDB instance. The class uses .CloseAndStop() only
when it is about to raise an exception.

All inputs are verified to make sure later statements can process them. Exceptions are raised only when the
program cannot continue. All methods behave like expected, if .CloseCollection() is invoked and there is not
collection connection to close, the method will return the same value as if it has closed an existing
connection.

### DatabaseConfig

DatabaseConfig is a resource file where all file paths required for proper operation of DatabaseController
are specified.


