#!/usr/bin/env python
#10/10/2018 V 0.3 KV
# Copyright reserved kv2000in@gmail.com
# To do : - 1) Check the type of file being uploaded - Remove  malicious files
#2) Add more vital signs on the html page.
#3) Separate SBP/DBP from NIBP and ABP
#4) Delete uploaded files once the scraping has finished

import cgi, os, sys
import cgitb
#### Remove after debugging
#cgitb.enable()
######### Remove after debugging
import re

try: # Windows needs stdio set for binary mode.
	import msvcrt
	msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
	msvcrt.setmode (1, os.O_BINARY) # stdout = 1
except ImportError:
	pass

form = cgi.FieldStorage() # List of all the fields in the form

fileitem = form['file'] # Get the input with name 'file' in the submitted form

#Scrapper function matches the regex and fills up the output file
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
# Test if the file was uploaded
if fileitem.filename:
	
	# strip leading path from file name
	# to avoid directory traversal attacks
	fn = os.path.basename(fileitem.filename)
	open('tmp/' + fn, 'wb').write(fileitem.file.read())
	#message = 'The file "' + fn + '" was uploaded successfully'
	#File has been uploaded - get the list of vital signs
	VitalSigns = form.getlist('VitalSign')
	myWfile= open('tmp/'+fn+'.csv', 'w')
	myRfile = open('tmp/' + fn)
	for eachline in myRfile:
		for eachVS in VitalSigns:
			scrapper(eachline,eachVS)
	#close the files when the job is done
	myRfile.close()
	myWfile.close()
	sys.stdout.write( "Content-type: text/csv\r\nContent-Disposition: attachment; filename="+fn+".csv\r\n\r\n" + file('tmp/'+fn+'.csv',"rb").read() )
else:
	message = 'No file was uploaded'
	print """\
		Content-Type: text/html\n
		<html><body>
		<p>%s</p>
		</body></html>
		""" % (message,)




