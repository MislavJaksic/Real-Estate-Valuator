Database
========

Database is where the system stores data which it then uses for analysis. The system's architecture allows the database to be swapped with a different database.

Mongo Database
--------------
Mongo database is the database that the system currently uses to store data. Mongo database is accessed through a driver called Pymongo. Pymongo is abstracted in Database.py.

Database.py
-----------
Database.py is a very robust and abstract group of methods that control access to Mongo database. Database.py makes sure Mongo database is online and that it closes properly if an exception occurs. A normal use case is: create database object, open connection, access the database and then close connection.

