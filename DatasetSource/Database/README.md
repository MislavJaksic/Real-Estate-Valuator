## Database

MongoDB is the database that the system currently uses. MongoDB is accessed through DatabaseController which
in turn uses Pymongo, a database driver.

### DatabaseController

DatabaseController was created to handle turning on the [mongod process](https://docs.mongodb.com/manual/reference/program/mongod/) and turning it off by releasing
locks as well as to abstract common queries such as Insert() and Find(). All inputs are verified, exceptions are
raised only if the program cannot continue and all methods pretend as if their code has been executed even if
it wasn't (for example: if a user invokes .Close() to close a connection to the database even if such connection
doesn't exist, the method will return the same values as if it closed a connection that did exist).

### DatabaseConfig

DatabaseConfig is a resource file where all file paths required for proper operation of DatabaseController
are specified.


