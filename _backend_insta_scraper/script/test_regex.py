#!/usr/bin/python
import re

line = """bb cc Cats are smarter than dogs
dfsf sdf sdf sdfds """;

searchObj = re.search( r'(.*) are (.*?) .*?', line, re.M|re.I)

if searchObj:
   print ("searchObj.group() : ", searchObj.group())
   print ("searchObj.group(1) : ", searchObj.group(1))
   print ("searchObj.group(2) : ", searchObj.group(2))
else:
   print ("Nothing found!!")



str = 'an example word:c54t!!'
match = re.search(r'word:\w\w\w', str)
# If-statement after search() tests if it succeeded
if match:
  print ('found', match.group()) ## 'found word:cat'
else:
  print ('did not find')
