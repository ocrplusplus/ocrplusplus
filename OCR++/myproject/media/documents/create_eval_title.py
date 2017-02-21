
from __future__ import division

import xml.etree.ElementTree as ET

directory = '/var/www/html/OCR++/myproject/media/documents/'

# """
# Create an summary file of author names
# """
def genFile(fName, path=""):
    tree = ET.parse(directory + "TitleAuthor.xml")
    root = tree.getroot()
    f = open(directory + 'eval_title.txt','w')
    t = root.findall('title')
    f.write("<<title>>\n")
    if(len(t)>0):
    	# import codecs
    	# content = unicode(t[0].text.strip(codecs.BOM_UTF8), 'utf-8')
    	# ti = unicodedata.normalize('NFKD',t[0].text).encode('ascii','ignore')
    	f.write("Title : ")
    	f.write(t[0].text.strip('\n,\t').encode('utf8'))
    	f.write("\n")
    f.close()
    # print "Done!!!"


# """Demo call"""
genFile("TitleAuthor.xml")