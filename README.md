Sparkify Data Analytics Project:
====

Summary:
----

The objective of this project is to create a database for analyitics on the use of our service. More specifically, the project will consist on recovering data from multiple data files we have been collecting for some time and inserting them in a database, which will be created with this purpose. By having all the data readily available in a relational database we will be able to perform a great variety of queries to make sense of this data and bring value to our company, by better understanding how our service is being used.

Parts of the project:
---

**sql_queries.py:** this file contains all the queries which will be used to drop and create tables, as well as to insert data in the tables. By grouping them in a single file, we can easily modify them without worrying about forgetting to change it somewhere else.

**create_tables.py:** WARNING: this file prepares the database for loading data, BY DROPPING ALL currently existing data and tables first. Please make sure there is nothing there that cannot be easily recovered, or stored in the source files. After dropping all tables, it creates the empty tables again ready to be filled with data.

**etl.py:** this file extracts all the data from the multiple source files and inserts them into the tables previously created. We first need to run create_tables.py for this script to work.

**test.ipynb:** this file can be run to verify if the data has been correctly loaded in the tables.

**etl.ipynb:** this file was used to create the etl.py file, but is of no further use in the project.

**data:** this folder should contain all the data we wish to load on to the database. The data should be split in two folders, log_data and song_data and the internal structure of these folders should be as per company policy,...

Running the code:
---
Open a python console and run the following files in order:
1. create_tables.py
2. etl.py
3. if necessary, test.ipynb
Note that to run the files we must use a Python console. Within the project workspace, we can easily open one, then we type *%run filename*

Schema Design and ETL Pipeline:
---

The source data is divided in two datasets, called song_dataset and log_dataset respectively. The first contains information on the songs, such as the song name, the artist name and the album, and the second one contains data on the events that have taken place within the system (song reproductions) and information on the users which perform these events, such as the users firstname, lastname and gender, the user agent, or the time of the event. The first dataset has been used to build the songs table and the artists table. The second has been used to build the rest of the tables.

The way this data is stored in the database has been thought in order to reduce the duplicated information, thus putting in place a star schema with one fact table (songplays) and four dimension tables (user, song, artist and time). The songplays table contains the data related to the reproduction event in the service, and the rest of the tables complement this information with data which would otherwise be recurring related with the song, the user and the artist, which tend to change less often. Timestamps for the events are stored in the time dimension table. The songplays table is connected to all the rest because it contains all of their keys: *start_time*, *user_id*, *song_id* and *artist_id*. The only other table which has a foreign key is the songs table which has the *artist_id* foreign key connecting it to the artists table.

**Dimension Tables:**

They contain mostly the data which would be recurrently stored in an event table, as they don't usually change from event to event. The column names appear in *italics*.

**TABLE users:** contains information about the users in the app such as *user_id* (which will the primary key for this table), *first_name*, *last_name*, *gender* and *level* (paid or free use of service). Example:

![users_table_sample](/screenshots/users_table_sample.png)

**TABLE songs:** contains information about the songs contained in the music database and include *song_id* (again, the primary key), *title*, *artist_id* (foreign key for the artist table), the *year* it was recorded, and its *duration*. Example:

![songs_table_sample](/screenshots/songs_table_sample.png)

**TABLE artists:** contains information on the artists in the music database: *artist_id* (primary key), *name* of the artist, *location* of the artist, *longitude* and *latitude* of this location. Example:

![artists_table_sample](/screenshots/artists_table_sample.png)

**TABLE time:** contains the timestamps of the records in songplays, but broken up by time units: *start_time* (absolute time in ms of the event and primary key), *hour*, *day*. *week* of the year, *month*, *year*, *weekday*. Example:

![time_table_sample](/screenshots/time_table_sample.png)


**Fact Table: songplays**

We have only one fact table called songplays. This table contains information from the log data associated with song plays (only those events marked with *page*=NextSong). The table has the following columns: *songplay_id* (**PK**), *start_time* (**FK**), *user_id* (**FK**), *level*, *song_id* (**FK**), *artist_id* (**FK**), *session_id*, *location* and *user_agent*. The primary key, *songplay_id* is generated when introducing the data in the table using the SERIAL type. Example:

![songplays_table_sample](/screenshots/songplays_sample.png)


About the Dataset:
---

The datasets which is used to build as tables are structured as follows:

**song_dataset:**
![song_dataset_sample](/screenshots/song_dataset_sample.png)

**log_dataset:**
![log_dataset_sample](/screenshots/log_dataset_sample.png)

**Dataset Cleaning:**

The restrictions on the columns marked as NOT NULL (which are ALL the primary keys in this case) as well as the typing, ensure that the essential data has the correct type and that all essential data is loaded, or no data is loaded at all, effectively cleaning the dataset for incomplete rows. No further measures for data cleaning have been taken.