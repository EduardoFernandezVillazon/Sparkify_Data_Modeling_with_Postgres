import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    
    """ This function opens the song_data files and loads them to create the song data and artist data which will be loaded to the database.\
        It also executes the query to insert this data."""
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[[
        'song_id', 'title',
        'artist_id', 'year', 
        'duration'
        ]].values[0].tolist()
    
    #song_data = [item for sublist in song_data for item in sublist] kept for learning purposes
    
    cur.execute(
        song_table_insert, 
        song_data)
    
    # insert artist record
    artist_data = df[[
        'artist_id', 'artist_name', 
        'artist_location', 'artist_latitude', 
        'artist_longitude'
        ]].values[0].tolist()
    
    #artist_data = [item for sublist in artist_data for item in sublist] kept for learning purposes
    
    cur.execute(
        artist_table_insert, 
        artist_data)


def process_log_file(cur, filepath):
    
    """This function opens the log_data files and loads them to create the time data, user data and songplay data which will be loaded to the database.\
        It also executes the query to insert this data."""
    
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page']=='NextSong']

    # convert timestamp column to datetime
    t = df['ts']
    t= pd.to_datetime(t,unit='ms')
    
    # insert time data records
    time_data = [
        df.ts,t.dt.hour,
        t.dt.day,t.dt.weekofyear,
        t.dt.month,t.dt.year,
        t.dt.weekday
        ]
    
    column_labels = (
        "start_time","hour",
        "day","week",
        "month","year",
        "weekday"
        )
    
    time_df = pd.DataFrame(dict(zip(column_labels, time_data)))
    
    #time_df = pd.DataFrame(time_data).T kept for learning purposes
    #time_df.columns=column_labels kept for learning purposes

    for i, row in time_df.iterrows():
        cur.execute(
            time_table_insert, 
            list(row)
            )

    # load user table
    user_df = df[[
        'userId','firstName',
        'lastName','gender',
        'level'
        ]]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(
            user_table_insert, 
            row
            )

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(
            song_select, 
            (row.song, row.artist, row.length)
        )
        
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (
            row.ts, row.userId, row.level, 
            songid, artistid, row.sessionId, 
            row.location, row.userAgent 
            )
        
        cur.execute(
            songplay_table_insert, 
            songplay_data
            )


def process_data(cur, conn, 
                 filepath, func):
    """This function runs through all the data files stored in the filepath, and then runs the process_song_file or the process_song_file function in order to extract and insert all data for each file. \
    \
    This function will retrieve all the filepaths for the different data files and sends the other two functions the exact filepath for each individual file. """
    # get all files matching extension from directory
    all_files = []
    
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    
    """The main function creates the connection to the database, calls the function to process the data, then closes the connection to the database."""
    
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(
        cur, conn, 
        filepath='data/song_data', 
        func=process_song_file
        )
    
    process_data(
        cur, conn, 
        filepath='data/log_data', 
        func=process_log_file
        )

    conn.close()


if __name__ == "__main__":
    main()