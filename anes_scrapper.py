#!/usr/bin/python
#10/10/2018 KV v0.3
#To do:
#1) Automate file name for csv , check for existing file name etc.
#2) Clean up encoding - solved by importing data as text/unicode:65001  in Excel
#3) User sends http request - gets a webpage with a file upload
#4 On uploading the file - user is asked to select the vital signs to extract from a list of vital signs. Once the user hits submit - python script is run with uploaded file and user selected parameters and then the results are returned to the user in a .csv file format.


import sys #sys.argv[0] is file name arg1 = sys.argv[1]
import re
def scrapper(myline,mystring):
	myregex  = re.escape(mystring)+r':\s*(\S*)\s?(.{0,10})\s\(Device Time: (..:..:..)\)'
	mytxt = re.search(myregex,myline)
	mysaveddata=""
	if (mytxt):
		#Replace the "non-breaking hyphen" with "-" - if it is present in the value string
		#mytxt.group(1).replace("\xe2\x80\x91","-")
		#If we have a match - create the row for CSV file
		mysaveddata = mystring+","+mytxt.group(3)+","+mytxt.group(1)+","+mytxt.group(2)+"\n"
		myWfile.write(mysaveddata)
#If arg list is empty - show usage
if len(sys.argv) == 1:
	print("Add the Vital Signs you need extracted from this file")
	print("For eg : to extract NIBP and ABP data - this script should be run as follows")
	print("/anes_scrapper.py CVP ABP NIBP 'NIBP (Mean)'")
	print("Vital signs passed here in arguments should be EXACT MATCH. For eg: if data is stored as NIBP and you type nibp - won't work. If you want NIBP (Mean) extracted - type it exactly like that")
	print("it will produce a .csv file with Vital values, units and timestamps")
	print("data from .CSV file can be easily imported into Excel sheets")
else:

	#Open a CSV file for writing
	myWfile= open("/Users/kv2000in/Downloads/anes_data.csv", 'a')

	#Open the file and start reading line by line
	myRfile = open("/Users/kv2000in/Downloads/anes_data.txt")
	for eachline in myRfile:
		#Run each line through the list of VitalSigns provided by the user
		for eachVS in sys.argv:
			scrapper(eachline,eachVS)
	#close the files when the job is done
	myRfile.close()
	myWfile.close()

