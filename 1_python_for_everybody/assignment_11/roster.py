#****************************************************************************************
# Instructions
# 
# This application will read roster data in JSON format, parse the file, and then produce 
# an SQLite database that contains a User, Course, and Member table and populate the 
# tables from the data file.
# 
# You can base your solution on this code: http://www.py4e.com/code3/roster/roster.py - 
# this code is incomplete as you need to modify the program to store the role column in 
# the Member table to complete the assignment.
# 
# Each student gets their own file for the assignment. Download this file and save it as 
# roster_data.json. Move the downloaded file into the same folder as your roster.py 
# program.
# 
# Once you have made the necessary changes to the program and it has been run 
# successfully reading the above JSON data, run the following SQL command:
# 
# SELECT User.name,Course.title, Member.role FROM 
#     User JOIN Member JOIN Course 
#     ON User.id = Member.user_id AND Member.course_id = Course.id
#     ORDER BY User.name DESC, Course.title DESC, Member.role DESC LIMIT 2;
# 
# The output should look as follows:
# 
# Zuriel|si430|0
# Zoya|si301|0
# 
# Once that query gives the correct data, run this query:
# 
# SELECT 'XYZZY' || hex(User.name || Course.title || Member.role ) AS X FROM 
#     User JOIN Member JOIN Course 
#     ON User.id = Member.user_id AND Member.course_id = Course.id
#     ORDER BY X LIMIT 1;
# 
# You should get one row with a string that looks like XYZZY53656C696E613333.
#****************************************************************************************

import sqlite3
import json

connection = sqlite3.connect('roster.sqlite')
cursor = connection.cursor()

# Drop tables in case they exist and create them after.
cursor.executescript(
    '''
    DROP TABLE IF EXISTS User;
    DROP TABLE IF EXISTS Course;
    DROP TABLE IF EXISTS Member;

    CREATE TABLE User (
        id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name   TEXT UNIQUE
    );

    CREATE TABLE Course (
        id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        title  TEXT UNIQUE
    );

    CREATE TABLE Member (
        user_id     INTEGER,
        course_id   INTEGER,
        role        INTEGER,
        PRIMARY KEY (user_id, course_id)
    )
    '''
)

# Ask for file name and read it.
fname = input('Enter file name: ')

if len(fname) < 1:
    fname = '../files/roster_data.json'

try:
    fhandler = open(fname)
    data = json.load(fhandler)
except:
    print('Wrong file name')
    quit()

for item in data:
    name = item[0]
    title = item[1]
    role = item[2]

    cursor.execute('INSERT OR IGNORE INTO User (name) VALUES (?)', (name,))
    cursor.execute('SELECT id from User WHERE name = ?', (name,))
    user_id = cursor.fetchone()[0]

    cursor.execute('INSERT OR IGNORE INTO Course (title) VALUES (?)', (title,))
    cursor.execute('SELECT id from Course WHERE title = ?', (title,))
    course_id = cursor.fetchone()[0]

    cursor.execute('INSERT OR REPLACE INTO Member (user_id, course_id, role) VALUES (?, ?, ?)', (user_id, course_id, role))
    
query = '''
    SELECT 'XYZZY' || hex(User.name || Course.title || Member.role ) AS X FROM 
    User JOIN Member JOIN Course 
    ON User.id = Member.user_id AND Member.course_id = Course.id
    ORDER BY X LIMIT 1;
'''

connection.commit()

for row in cursor.execute(query):
    print(row[0])

cursor.close()