from __future__ import division

import xml.etree.ElementTree as ET
directory = '/var/www/html/OCR++/myproject/media/documents/'


# """
# Create an summary file of author names
# """
def genFile(tit_aut_xml, path=""):
    root = ET.fromstring(tit_aut_xml)
    #root = tree.getroot()
    #f = open(directory + 'title_author.txt','w')
    output = ''
    for author in root.findall('name'):
        fn = author.findall('first_name')
        mn = author.findall('middle_name')
        ln = author.findall('last_name')
        # print "<<section>>"
        # f.write("<<name>>\n")
        #print fn[0].text.split()[0]
        if(len(fn)>0):
            #f.write("#f "+fn[0].text.split()[0]+"\n")
            output += "#f "+fn[0].text.split()[0]+"\n"
        if(len(mn)>0):
            #f.write("#m "+mn[0].text.strip('\t').strip('\n').strip('\t')+"\n")
            output += "#m "+mn[0].text.strip('\t').strip('\n').strip('\t')+"\n"
        if(len(ln)>0):
            #f.write("#l "+ln[0].text.split()[0]+"\n")
            output += "#l "+ln[0].text.split()[0]+"\n"
    #f.close()
    # print output
    return output
    #print "Done!!!"


#"""Demo call"""
#genFile("TitleAuthor.xml")