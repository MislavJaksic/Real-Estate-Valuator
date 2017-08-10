## Database

MongoDB is the database that the system currently uses. MongoDB is accessed through DatabaseController which
in turn uses Pymongo, a database driver.

### DatabaseController

DatabaseController was created to handle turning on the [mongod process](https://docs.mongodb.com/manual/reference/program/mongod/) and turning it off by releasing
locks as well as to abstract common queries such as Insert() and Find(). All inputs are verified, exceptions are
raised only if the program cannot continue and all methods pretend as if their code has been executed even if
it wasn't (for example: if a user invokes .Close() to close a connection to the database even if such connection
doesn't exist, the method will return the same values as if it closed a connection that did exist).

Responsibilities: Find() documents in an open collection, Insert() documents into an open collection, Inspect() MongoDB to find what's in it. Open() opens a connection to a collection and makes sure there is only one collection connection open per object. The class creates a MongoDB instance when functions require it. The class makes sure there is only one such instance running at any time. Close() closes the MongoDB instance "gently" to make it release it's locks and save data.

It is up to the user to use Close() to close the MongoDB instance. The class uses Close() only when it is about to raise an exception.

### DatabaseConfig

DatabaseConfig is a resource file where all file paths required for proper operation of DatabaseController
are specified.


