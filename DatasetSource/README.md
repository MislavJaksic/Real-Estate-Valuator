## Dataset Source

Datasets can be stored in different forms. There are two common ways of storing large amounts of data. The first
is to use a database and the other is to store data in a file. 

### Database

The database that the system uses is called [MongoDB](https://docs.mongodb.com/). It was installed together with a python driver
called [Pymongo](https://docs.mongodb.com/ecosystem/drivers/python/). The system can switch to using a different database with minimal changes.

### File

File is where all dataset files will be stored. Files with different extensions have different ways of
organising data within the file.

### DatasetLoader

DatasetLoader is responsible for implementing functions which load data from a specified source, prepare it
for insertion into a Pandas DataFrame and load it into Pandas DataFrame.

