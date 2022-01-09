#****************************************************************************
# 8.4 Open the file romeo.txt and read it line by line. For each line, split 
# the line into a list of words using the split() method. The program should 
# build a list of words. For each word on each line check to see if the word 
# is already in the list and if not append it to the list. When the program 
# completes, sort and print the resulting words in alphabetical order.
# You can download the sample data at http://www.py4e.com/code3/romeo.txt
#****************************************************************************

fname = input("Enter file name: ")

try:
    fhandler = open(fname)
except:
    print('Wrong file name')
    quit()

list = list()

# Get words in lines. If the word does not exist in the list, add it.
for line in fhandler:
    split_line = line.strip().split()

    for word in split_line:
        if word in list:
            continue

        list.append(word)

# Sort list.
list.sort()

print(list)