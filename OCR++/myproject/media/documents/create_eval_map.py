from __future__ import division

import xml.etree.ElementTree as ET

directory = '/var/www/html/OCR++/myproject/media/documents/'

# """
# Create an summary file of maps
# """
def genFile(fName, path=""):
	tree = ET.parse(directory + "map.txt")
	root = tree.getroot()
	f = open(directory + 'eval_map.txt','w')
	for m in root.findall('map'):
		# print m.text
		f.write("<<map>>\n")
		if(len(m.text)>0):
			t = m.text.split('\n')
			# print t[1].strip('\n,\t')
			f.write("Author : "+ t[1].strip('\n,\t')+"\n")
			f.write("Email  : "+ t[2].strip('\n,\t')+"\n")
	f.close()
	# print "Done!!!"


"""Demo call"""
genFile("map.txt")