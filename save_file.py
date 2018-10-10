#!/usr/bin/env python
import cgi, os
import cgitb; cgitb.enable()
import re

try: # Windows needs stdio set for binary mode.
	import msvcrt
		msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
		msvcrt.setmode (1, os.O_BINARY) # stdout = 1
except ImportError:
	pass

form = cgi.FieldStorage()

# A nested FieldStorage instance holds the file
fileitem = form['file']

# Test if the file was uploaded
if fileitem.filename:
	
	# strip leading path from file name
	# to avoid directory traversal attacks
	fn = os.path.basename(fileitem.filename)
	open('tmp/' + fn, 'wb').write(fileitem.file.read())
	message = 'The file "' + fn + '" was uploaded successfully'

else:
	message = 'No file was uploaded'

print """\
	Content-Type: text/html\n
	<html><body>
	<p>%s</p>
	</body></html>
	""" % (message,)

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
myWfile= open('tmp/'+fn+'.csv', 'w')
myRfile = open('tmp/' + fn)
	#	for eachline in myRfile:
	#	for eachVS in sys.argv:
	#		scrapper(eachline,eachVS)
	#close the files when the job is done
	myRfile.close()
	myWfile.close()
