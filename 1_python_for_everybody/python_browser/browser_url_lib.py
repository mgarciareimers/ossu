import urllib.request, urllib.parse, urllib.error

handler = urllib.request.urlopen('http://www.dr-chuck.com/page1.htm')

for line in handler:
    print(line.decode().strip())