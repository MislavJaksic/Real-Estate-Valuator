## Project documentation

### Problem

In Croatia, real estate evaluation is expensive, takes a long time and is based on data hidden in a database
unavailable to the public.

### Requirements and functionalities

Scrape real estate data from websites.
Store data for analysis.
Deleted data after it has been analysed.
Load data into data analysis tool.

Count the number of times a value has occurred in each variable.
Count the number of missing values in each variable.
Draw graphs, distribution, boxes, scatter.

Transform data based on values.

Construct a prediction model using machine learning.
Predict the price of an unknown property.

Specify property data through a graphical interface.
Receive price prediction through a graphical interface.

### Architecture

- Program organisation - the system is divided into the following building blocks: DatasetSources, DatasetAnalysis,
DatasetTransformation, Predicting, Graphical User Interface (GUI), InputControl and Tests.
  - DatasetSources role is to store data in a file or a database as well as to load data for use by other
building blocks.
  - DatasetAnalysis role is to visualize values in a dataset through graphs and count the number of times a
value occurs.
  - DatasetTransformation role is to implement commonly used methods for transforming data and to store
scripts that will transform the data.
  - Predicting role is to use machine learning to develop a model that will correctly predict the price of an
apartment.
  - GUI role is to allow users to interact with the valuation system by letting them input information about
their apartments and displaying the predicted price of the apartment.
  - InputControl role is to check if the parameter values can be used by the method.
  - Tests role is to unit test each method and make sure they behave as intended.

- Major classes -

- Data design - Data is stored in a database called MongoDB. The database is used instead of a .cvs file is because
this project is a perfect time to learn how to use a noSQL database. MongoDB was choosen because it has a driver
called Pymongo that communicates with the database through Python. PostgreSQL was also considered due to its
popularity, but a scraper library, Scrapy, has a tutorial on how to use it with MongoDB and Pymongo.

- Business rules - there are no rules that had to be implemented as the purpose of the system is to give users a rough
idea of how much their property is worth and not to generate a binding document that would determine the value of
the property.

- User interface - the GUI is made up of four rows. The first row is filled with labels that label the drop down menus
in the second row. Drop down menus are used because they eliminate the need to checking input. The alternative to
drop down menus is a text box into which the user could write a value, but then the values would have to be
validated. There is a button in the third row that begins the property valuation process. The forth row is where the
label with the price prediction will appear after the property has been valuated.

- Resource management - on Windows, using the system will take up about 80MB of RAM, but depending on the size of the
dataset, it could be up to 100MB. The system makes sure there is only one connection to a database at any one time.

- Security - I don't know enough about this topic to think about it.

- Performance - the system takes up a lot of memory to increase the speed and additional memory can be sacrificed to
increase the speed even further by saving the machine learned model and then using it when the query that uses the
same data is made instead of constructing the model from scratch.

- Scalability - the system is made for Windows and the increase in the number of users will have negligible effect on
the system.

- Internationalisation and localisation - the system uses UTF-8 because the Croatian alphabet uses characters that are
not covered by ASCII. The strings displayed on the GUI can be translated to another language by creating a resource
file that would be used by as a dictionary and implementing a method that would do the translation.

- Input and output - the external data inputs don't have to be checked because they are received through a GUI's drop
down menus. Each method is responsible for validating their own input using a single InputController class that
handles validation centrally.

- Error processing - errors are detected, not corrected and when they are detected the system either raises an
exception and performs an action before quitting or return a neutral value that will have a benigne effect on the
rest of the system. 

- Fault tolerance - the system is very fault tolerant as all external inputs are validated, most internal inputs are
validated and if the error occurs, the system shuts down gracefully.

- Architectural feasibility - it is feasible to construct the system. Proving that is something I don't know how to do,
except by constructing the system.

- Overengineering and robustness - the system will shut down if it detect an error when attempting to communicate with
the database, but in all other cases the system continue to work, but will return a neutral value to signal an error
has occurred. 

- Buy vs build decision - the system uses the following external libraries: Pymongo, pandas, seaborn, PyQt5 and
sklearn. Pymongo is a driver that allows Python to communicate with the database MongoDB. pandas is a library made
for exploring and transforming data in tabular form. seaborn is a library that allows users to visualize data. PyQt5
is a library that facilitates the creation of graphical user interfaces. sklearn implements state of the art machine
learn algorithms. The rest of the system is written in Python and connects all the libraries.

- Reuse decision - all programs can be reused except for the Predictor and parts of the ValueateApartment programs for
analysing other datasets. Predictor cannot be reused because it is tailor made for a single dataset as is a part of
the ValuateApartment.

- Change strategy - the building blocks of the system are loosely coupled which means changing a part of the system is
very easy and quick. Tests are implemented to make sure the changed are implemented correctly. A possible
enhancement is a methods that would handle loading data from files. The system is built with adding new data in
mind and so if a new dataset is added, the system wouldn't have to change in more then two places: GUI and Predictor.

- General architectural quality - 

### Programming conventions

The naming convention is called CamelCase.

Classes, methods and function have the first letter of each word capitalized. Example: GetAttribute()
Local variables and parameters have the first letter of each word capitalized except for the first word. Example:
firstName
