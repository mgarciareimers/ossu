#****************************************************************************************
# Counting Organizations
#
# This application will read the mailbox data (mbox.txt) and count the number of email 
# messages per organization (i.e. domain name of the email address) using a database with 
# the following schema to maintain the counts.
# 
# CREATE TABLE Counts (org TEXT, count INTEGER)
#
# When you have run the program on mbox.txt upload the resulting database file above for 
# grading.
# If you run the program multiple times in testing or with dfferent files, make sure to 
# empty out the data before each run.
# 
# You can use this code as a starting point for your application: 
# http://www.py4e.com/code3/emaildb.py.
# 
# The data file for this application is the same as in previous assignments: 
# http://www.py4e.com/code3/mbox.txt.
# 
# Because the sample code is using an UPDATE statement and committing the results to the 
# database as each record is read in the loop, it might take as long as a few minutes to 
# process all the data. The commit insists on completely writing all the data to disk 
# every time it is called.
# 
# The program can be speeded up greatly by moving the commit operation outside of the 
# loop. In any database program, there is a balance between the number of operations you 
# execute between commits and the importance of not losing the results of operations that 
# have not yet been committed.
#****************************************************************************************

import sqlite3

connection = sqlite3.connect('emaildb.sqlite')
cursor = connection.cursor()

# Drop table in case it exists and create it after.
cursor.execute('DROP TABLE IF EXISTS Counts')
cursor.execute('CREATE TABLE Counts (org TEXT, count INTEGER)')

# Ask for file name and read it.
fname = input('Enter file name: ')

if len(fname) < 1:
    fname = 'mbox-short.txt'

try:
    fhandler = open(fname)
except:
    print('Wrong file name')
    quit()

# Count organizations.
organization_count_dict = dict()

for line in fhandler:
    #if not line.startswith("From "):
    if not line.startswith("From:"):
        continue
    

    try:
        #split_line = line.strip().split()[1].split('@')
        split_line = line.strip().split('@')
        organization_count_dict[split_line[1]] = organization_count_dict.get(split_line[1], 0) + 1
    except:
        continue

# Insert organizations into database.
for organization,count in organization_count_dict.items():
    cursor.execute('INSERT INTO Counts (org, count) VALUES (?, ?)', (organization, count))

connection.commit()

# Select data from database.
query = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cursor.execute(query):
    print(str(row[0]), row[1])

cursor.close()