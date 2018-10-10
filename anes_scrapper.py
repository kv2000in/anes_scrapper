#!/usr/bin/python
# -*- coding: utf-8 -*-
#10/8/2018 KV v0.1
# Open the file --> Read it line by line --> run each line through the scrapper function
# Scrapper function --> Iterate the line over/Match a pre-defined set of strings (supplied via sys.argv[] with this line (in web based application - user can select which "headings" the user want to scrape from the file) --> if found -->store the corresponding value, unit, device time.
# For example - a typical line would be "HR: 58 (Device Time: 07:17:09) PIP: 21 (Device Time: 07:17:11)"
# Make a dictionary for each of the sys.argv[] and store value, unit, time


'''
>>> mystring ="HR"
>>> myline = "HR: 58 (Device Time: 07:17:09) PIP: 21 (Device Time: 07:17:11)"
>>> myregex = re.escape(mystring)+r':\s(-?[0-9]*[A-Za-z]*)\s\(D'
>>> mytxt = re.search(myregex, myline)
>>> print(mytxt.group(1))
58
myregex = re.escape(mystring)+r':\s(-?[0-9]*[A-Za-z]*)\s\(D' 
Match mystring followed by ": " 
followed by space "\s" 
then start capturing into group "(" 
then optional "-" sign, preceding character made optional by ? 
then numbers [0-9] quantified by * meaning any number of numbers 
followed by any number of letters [A-Za-z]* 
stop capturing ")" 
followed by space"\s" 
followed by "\(" need to use the escape character before ( 
followed by letter D
>>> myline="PAP-M: ‑27 (Device Time: 07:18:09) CVP:  ‑21 mmHg (Device Time: 07:18:09)"
>>> mystring="CVP"
>>> myregex = re.escape(mystring)+r':\s*(\S*)\s?(\S*)\s\(Device\sTime:\s(.*)\)'
>>> mytxt = re.search(myregex, myline)
>>> print(mytxt.group(1))
‑21
>>> print(mytxt.group(2))
mmHg
>>> print(mytxt.group(3))
07:18:09
>>> 
>>> mystring="PAP-M"
>>> myregex = re.escape(mystring)+r':\s*(\S*)\s?(\S*)\s\(Device\sTime:\s(.*)\)'
>>> mytxt = re.search(myregex, myline)
>>> print(mytxt.group(1))
‑27
>>> print(mytxt.group(2))

>>> print(mytxt.group(3))
07:18:09) CVP:  ‑21 mmHg (Device Time: 07:18:09
>>> 
>>> myregex = re.escape(mystring)+r':\s*(\S*)\s?(\S*)\s\(Device\sTime:\s(..:..:..)\)'
>>> mytxt = re.search(myregex, myline)
>>> print(mytxt.group(3))
07:18:09
>>> print(mytxt.group(2))

>>> print(mytxt.group(1))
‑27
### Initial regex
#r':\s*(\S*)\s?(\S*)\s\(Device\sTime:\s(.*)\)'
: followed by any number of white space \s*
start capturing group 1 (
followed by any number of non White space char \S*
complete capture group 1 )
followed by optional white space char \s?
start capturing group 2 (
followed by any number of non White space char \S*
complete capture group 2 )
followed by space \s
followed by \(Device\sTime:\s ## ( character is escaped by \
start capturing group 3 (
followed by any number of chars .*
complete capture group 3 )
followed by \)
#
### Changed to this regex
r':\s*(\S*)\s?(\S*)\s\(Device\sTime:\s(..:..:..)\)'

>>> myline = "ETCO2: 0 mmHg (Device Time: 07:18:09) FiO2: 100 % (Device Time: 07:18:09)"
>>> mystring="FiO2"
>>> myregex = re.escape(mystring)+r':\s*(\S*)\s?(\S*)\s\(Device\sTime:\s(..:..:..)\)'
>>> mytxt = re.search(myregex, myline)
>>> print(mytxt.group(1))
100
>>> print(mytxt.group(2))
%
>>> print(mytxt.group(3))
07:18:09
>>> mystring="ETCO2"
>>> myregex = re.escape(mystring)+r':\s*(\S*)\s?(\S*)\s\(Device\sTime:\s(..:..:..)\)'
>>> myregex = re.escape(mystring)+r':\s*(\S*)\s?(\S*)\s\(Device\sTime:\s(..:..:..)\)'
>>> mytxt = re.search(myregex, myline)
>>> print(mytxt.group(1))
0
>>> print(mytxt.group(2))
mmHg
>>> print(mytxt.group(3))
07:18:09
>>> 
>>> myline = "HR: 58 (Device Time: 07:17:09) PIP: 21 (Device Time: 07:17:11)"
>>> mystring="HR"
>>> myregex = re.escape(mystring)+r':\s*(\S*)\s?(\S*)\s\(Device\sTime:\s(..:..:..)\)'
>>> mytxt = re.search(myregex, myline)
>>> print(mytxt.group(1))
58
>>> print(mytxt.group(2))

>>> print(mytxt.group(3))
07:17:09
>>> mystring="PIP"
>>> mytxt = re.search(myregex, myline)
>>> print(mytxt.group(1))
58
>>> print(mytxt.group(2))

>>> print(mytxt.group(3))
07:17:09
>>> 
>>> myline = "NIBP: 111/77 (Device Time: 07:19:09) Mean Airway Pressure: 7 (Device Time: 07:19:18) "
>>> mystring="NIBP"
>>> myregex = re.escape(mystring)+r':\s*(\S*)\s?(\S*)\s\(Device\sTime:\s(..:..:..)\)'
>>> mytxt = re.search(myregex, myline)
>>> print(mytxt.group(1))
111/77
>>> print(mytxt.group(2))

>>> print(mytxt.group(3))
07:19:09
>>> myline = "NIBP (Mean): 85 (Device Time: 07:19:09) HR: 81 (Device Time: 07:19:09)"
>>> mystring="NIBP (Mean)"
>>> myregex = re.escape(mystring)+r':\s*(\S*)\s?(\S*)\s\(Device\sTime:\s(..:..:..)\)'
>>> print(mytxt.group(1))
111/77
>>> mytxt = re.search(myregex, myline)
>>> print(mytxt.group(1))
85
>>> print(mytxt.group(2))

>>> print(mytxt.group(3))
07:19:09
>>> 
'''
import sys #sys.argv[0] is file name arg1 = sys.argv[1]
import re
import csv
mydict = {}
def scrapper(myline,mystring):
	myregex  = re.escape(mystring)+r':\s*(\S*)\s?(.{0,10})\s\(Device Time: (..:..:..)\)'
	mytxt = re.search(myregex,myline)
	mysaveddata=""
	if (mytxt):
		mysaveddata = mytxt.group(3)+"|"+mytxt.group(1)+"|"+mytxt.group(2)
		#mydict["CVP"].append(mytxt.group(1))
		#print ("Value = ",end="") # Python 3 method of removing \n from the end
		'''
		print ("Value = "), # Trailing "," is Python 2 method of removing \n from the end
		print (mytxt.group(1)), 
		#print (" | ", end = "")        
		print ("|"),
		#print ("Unit = ",end="")
		print ("Unit = "),
		print (mytxt.group(2)), 
		#print (" | ", end = "")
		print ("|"),
		#print ("Time = ",end="")
		print ("Time = "),
		print (mytxt.group(3))
		'''
		mydict[mystring].append(mysaveddata)

# Create all the lists according to the user supplied list of Vital Signs
for eachVitalSign in sys.argv:
	mydict[eachVitalSign]=[]
#Open the file and start reading line by line
myfile = open("/Users/kv2000in/Downloads/anes_data.txt")
for eachline in myfile:
	#Run each line through the list of arguments
	for eachVS in sys.argv:
		scrapper(eachline,eachVS)



	

