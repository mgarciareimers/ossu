#****************************************************************************************
# Musical Track Database
#
# This application will read an iTunes export file in XML and produce a properly 
# normalized database with this structure:
# 
# CREATE TABLE Artist (
#     id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
#     name    TEXT UNIQUE
# );
# 
# CREATE TABLE Genre (
#     id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
#     name    TEXT UNIQUE
# );
# 
# CREATE TABLE Album (
#     id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
#     artist_id  INTEGER,
#     title   TEXT UNIQUE
# );
# 
# CREATE TABLE Track (
#     id  INTEGER NOT NULL PRIMARY KEY 
#         AUTOINCREMENT UNIQUE,
#     title TEXT  UNIQUE,
#     album_id  INTEGER,
#     genre_id  INTEGER,
#     len INTEGER, rating INTEGER, count INTEGER
# );
#
# If you run the program multiple times in testing or with different files, make sure to 
# empty out the data before each run.
# 
# You can use this code as a starting point for your application: 
# http://www.py4e.com/code3/tracks.zip. The ZIP file contains the Library.xml file to be 
# used for this assignment. You can export your own tracks from iTunes and create a 
# database, but for the database that you turn in for this assignment, only use the 
# Library.xml data that is provided.
# 
# To grade this assignment, the program will run a query like this on your uploaded 
# database and look for the data it expects to see:
# 
# SELECT Track.title, Artist.name, Album.title, Genre.name 
#     FROM Track JOIN Genre JOIN Album JOIN Artist 
#     ON Track.genre_id = Genre.ID and Track.album_id = Album.id 
#         AND Album.artist_id = Artist.id
#     ORDER BY Artist.name LIMIT 3
#
# The expected result of the modified query on your database is: (shown here as a simple 
# HTML table with titles)
# 
# |---------------------------------------------------------------------------|
# | Track	                                  | Artist |     Album    | Genre |
# |---------------------------------------------------------------------------|
# | Chase the Ace	                          | AC/DC  | Who Made Who | Rock  |
# | D.T.                                      |	AC/DC  | Who Made Who | Rock  |
# | For Those About To Rock (We Salute You)   |	AC/DC  | Who Made Who | Rock  |
# |---------------------------------------------------------------------------|
#****************************************************************************************

import sqlite3
import xml.etree.ElementTree as ET

# Method that finds a value by the key.
def find_value(track, key):
    found = False
    value = None

    for param in track:
        if found: 
            value = param.text
            break
        elif param.tag == 'key' and param.text == key:
            found = True

    return value

connection = sqlite3.connect('musical_tracks.sqlite')
cursor = connection.cursor()

# Drop tables in case they exist and create them after.
cursor.executescript(
    '''
    DROP TABLE IF EXISTS Artist;
    DROP TABLE IF EXISTS Genre;
    DROP TABLE IF EXISTS Album;
    DROP TABLE IF EXISTS Track;

    CREATE TABLE Artist (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT UNIQUE
    );

    CREATE TABLE Genre (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT UNIQUE
    );

    CREATE TABLE Album (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        artist_id  INTEGER,
        title TEXT UNIQUE
    );

    CREATE TABLE Track (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        title TEXT UNIQUE,
        album_id INTEGER,
        genre_id INTEGER,
        len INTEGER, rating INTEGER, count INTEGER
    );
    '''
)

# Ask for file name and read it.
fname = input('Enter file name: ')

if len(fname) < 1:
    fname = '../files/Library.xml'

try:
    data = ET.parse(fname)
except:
    print('Wrong file name')
    quit()

for track in data.findall('dict/dict/dict'):
    name = find_value(track, 'Name')
    artist = find_value(track, 'Artist')
    album = find_value(track, 'Album')
    genre = find_value(track, 'Genre')
    count = find_value(track, 'Play Count')
    rating = find_value(track, 'Rating')
    length = find_value(track, 'Total Time')

    if name is None or artist is None or album is None or genre is None:
        continue

    # Insert genre (if possible) and get id.
    cursor.execute('INSERT OR IGNORE INTO Genre (name) VALUES (?)', (genre,))
    cursor.execute('SELECT id from Genre WHERE name = ?', (genre,))
    
    genre_id = cursor.fetchone()[0]
    
    # Insert artist (if possible) and get id.
    cursor.execute('INSERT OR IGNORE INTO Artist (name) VALUES (?)', (artist,))
    cursor.execute('SELECT id from Artist WHERE name = ?', (artist,))
    
    artist_id = cursor.fetchone()[0]

    # Insert album (if possible) and get id.
    cursor.execute('INSERT OR IGNORE INTO Album (artist_id, title) VALUES (?, ?)', (artist_id, album))
    cursor.execute('SELECT id from Album WHERE title = ?', (album,))
    
    album_id = cursor.fetchone()[0]

    # Insert track.
    cursor.execute('INSERT OR REPLACE INTO Track (title, album_id, genre_id, len, rating, count) VALUES (?, ?, ?, ?, ?, ?)', (name, album_id, genre_id, length, rating, count))

connection.commit()

query = '''
    SELECT 
        Track.title, 
        Artist.name, 
        Album.title, 
        Genre.name 
    FROM 
        Track JOIN 
        Genre JOIN 
        Album JOIN 
        Artist 
    ON 
        Track.genre_id = Genre.ID AND 
        Track.album_id = Album.id AND 
        Album.artist_id = Artist.id
    ORDER BY 
        Artist.name 
    LIMIT 3
'''

for row in cursor.execute(query):
    print(str(row[0]), row[1])

cursor.close()