## Database Control

Database Control is responsible for spawning database processes, shutting them down, accessing and storing data
as well as any other functions that use the database. Database Control also ensures that if the current database
gets swapped with another database the only thing that would need to change is the DatabaseController.py program
and DatabaseConfig.py resource file.

### Mongo Database

Mongo database is the database that the system currently uses. Mongo database is accessed through
DatabaseController.py which in turn uses Pymongo, a database driver.

### DatabaseController

DatabaseController is robust. All inputs are verified, exceptions are raised only if the program cannot continue
and all methods pretend as if their code has been executed even if it wasn't (for example: if a user invokes
.Close() to close a connection to the database even if such connection doesn't exist, the method will return
the same values as if it closed a connection that did exist).

#### DatabaseController Use Case

- .Open(connection)
    - .Store(entry) OR
	- .GetDataIter(condition, distinct=False)
- .Close()

### DatabaseConfig

DatabaseConfig is a resource file that holds all the constants and file paths required for proper operation of
DatabaseController.py.

