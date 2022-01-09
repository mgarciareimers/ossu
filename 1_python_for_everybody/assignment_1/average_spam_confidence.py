#****************************************************************************
# 7.2 Write a program that prompts for a file name, then opens that file and 
# reads through the file, looking for lines of the form:
#
# X-DSPAM-Confidence:    0.8475
#
# Count these lines and extract the floating point values from each of the 
# lines and compute the average of those values and produce an output as 
# shown below. Do not use the sum() function or a variable named sum in your 
# solution. You can download the sample data at 
# http://www.py4e.com/code3/mbox-short.txt when you are testing below enter 
# mbox-short.txt as the file name.
#****************************************************************************

# Use the file name mbox-short.txt as the file name
fname = input("Enter file name: ")

try:
    fhandler = open(fname)
except:
    print('Wrong file name')
    quit()

total_lines = 0
confidence = 0

for line in fhandler:
    if not line.startswith("X-DSPAM-Confidence:"):
        continue
    
    # Count lines and extract confidence number.
    try:
        confidence = confidence + float(line[line.find(" "):].strip())
        total_lines = total_lines + 1
    except:
        continue

print("Average spam confidence:", confidence / total_lines)
