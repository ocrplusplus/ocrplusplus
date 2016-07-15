
from __future__ import division

import xml.etree.ElementTree as ET
directory = '/var/www/html/OCR++/myproject/media/documents/'


# """
# Create an summary file of author names
# """
def genFile(fName, path=""):
    tree = ET.parse(directory + "TitleAuthor.xml")
    root = tree.getroot()
    f = open(directory + 'eval_author.txt','w')
    for author in root.findall('name'):
        fn = author.findall('first_name')
        mn = author.findall('middle_name')
        ln = author.findall('last_name')
        # print "<<section>>"
        f.write("<<name>>\n")
        if(len(fn)>0):
            f.write("First name : "+fn[0].text.split()[0].encode('utf8')+"\n")
        if(len(mn)>0):
            f.write("Middle name : "+mn[0].text.strip('\t').strip('\n').strip('\t').encode('utf8')+"\n")
        if(len(ln)>0):
            f.write("Last name : "+ln[0].text.split()[0].encode('utf8')+"\n")
    f.close()
    # print "Done!!!"


"""Demo call"""
genFile("TitleAuthor.xml")