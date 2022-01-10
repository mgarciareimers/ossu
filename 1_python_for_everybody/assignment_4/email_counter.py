#****************************************************************************
# 9.4 Write a program to read through the mbox-short.txt and figure out who 
# has sent the greatest number of mail messages. The program looks for 
# 'From ' lines and takes the second word of those lines as the person who 
# sent the mail. The program creates a Python dictionary that maps the 
# sender's mail address to a count of the number of times they appear in the 
# file. After the dictionary is produced, the program reads through the 
# dictionary using a maximum loop to find the most prolific committer.
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
        dict[words[1]] = dict.get(words[1], 0) + 1
    except:
        continue

email = max(dict, key=dict.get)

print(email, dict[email])