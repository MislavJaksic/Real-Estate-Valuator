Database
========

Database is where the system stores data which it then uses for analysis. The system's architecture allows the database to be swapped with a different database.

Mongo Database
--------------
Mongo database is the database that the system currently uses to store data. Mongo database is accessed through a driver called Pymongo. Pymongo is abstracted in Database.py.

Database.py
-----------
Database.py is a very robust and abstract group of methods that control access to Mongo database. A normal use case is: create database object, open connection, access the database and then close connection.

Database.py methods
-------------------
The most important methods are:
Open(conn) - open a connection to a specific database and collection
Close() - close a connection and mongod
GetDataIter(condition, distinct) - get data iterator from the collection
Store(entry) - store an entry in the collection
Database.py takes care of booting up Mongo database and taking it offline as well as checking if a connection to a collection has been established.

