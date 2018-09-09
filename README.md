# Architecture
The programs are structured into 3 types of scripts:
-*params.py* holds information such as file paths,url links and html tags
-source scripts
	-*scrape_functions.py* stores functions that gets called and executed. 
		-There is a function to retrieve url from each auction event(the events in this case are March2018 and November2017).
		-There is another function to retrieve the information for each lot in every auction event. 
	-*queries.py* stores functions that answer the specific queries
-executing scripts
	-*extract_and_write_to_file.py* calls scraping functions and write dataset to file. It first turns all the data into a pandas dataframe, and then write to a csv file.   
	-*load_and_compute.py* loads the data into a pandas dataframe, and calls the required functions to answer the questions

# Data Warehousing
## Implemented
The data in this assignment is stored as a list of dictionaries, for the convenience of loading it as a dataframe. Given a wider scope, it is ideal to construct a database instance. Then a python-sql driver, such as psycopg2 will be used to connect to the sql instance for data analysis purposes.
## Suggested : Relational database with 2 entities
### Artist
This table stores information about the artists, including born-death information 
### Art_objects  	
This table stores information about the art pieces, with primary key being combination of lot number AND event. It will have foreign key of the artist id. It also holds the rest of the art attributes, such as title, sold and estimated price, etc.

# Assumptions
In forming similar object groups, we are assuming here that objects can repeat and be in more than one group, since it is impossible to create non-overlapping groups applying a single threshold. For example, object A is 5cm, object B is 15cm, object c is 25cm. with a threshold of 10, A and B are similar, B and C are similar, but A and C are not. Therefore there has to be a minimum of 2 groups, with each object appearing twice. 

# Other Improvements
## Switch to phantomjs from selenium for performance purposes
Current using selenium for simplicity and time-contraint.
## Add set-up script
This repository currently assumes a set of python modules and dependencies. With more time, a set_up.sh is useful to have, for packages installation and setting path. 


