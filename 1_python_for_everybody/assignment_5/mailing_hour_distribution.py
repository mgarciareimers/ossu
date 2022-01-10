#****************************************************************************
# 10.2 Write a program to read through the mbox-short.txt and figure out the 
# distribution by hour of the day for each of the messages. You can pull the 
# hour out from the 'From ' line by finding the time and then splitting the 
# string a second time using a colon.
#
# From stephen.marquard@uct.ac.za Sat Jan  5 09:14:16 2008
#
# Once you have accumulated the counts for each hour, print out the counts, 
# sorted by hour as shown below.
#****************************************************************************

fname = input("Enter file: ")

if len(fname) < 1:
    fname = "mbox-short.txt"

try:
    fhandler = open(fname)
except:
    print('Wrong file name')
    quit()

dict = dict()

for line in fhandler:
    if not line.startswith("From "):
        continue
    
    words = line.strip().split()

    try:
        hour = words[5].split(":")[0]
        dict[hour] = dict.get(hour, 0) + 1
    except:
        continue

sorted_time_list = sorted([ (k,v) for k,v in dict.items() ])

for k,v in sorted_time_list:
    print(k, v)