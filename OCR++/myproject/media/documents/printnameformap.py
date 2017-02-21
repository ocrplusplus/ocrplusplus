#####################################################################
# Generating author names in the format required by authorEmailMap  #
# Author: Barnopriyo Barua                                          #
# Email: barno0695@gmail.com                                        #
#####################################################################

from __future__ import division
import xml.etree.ElementTree as ET

directory = '/var/www/html/OCR++/myproject/media/documents/'

def genAuthorFileForMap(tit_aut_xml, path=""):
    root = ET.fromstring(tit_aut_xml)
    output = ''
    for author in root.findall('name'):
        fn = author.findall('first_name')
        mn = author.findall('middle_name')
        ln = author.findall('last_name')
        if(len(fn)>0):
            output += "#f "+fn[0].text.split()[0]+"\n"
        if(len(mn)>0):
            output += "#m "+mn[0].text.strip('\t').strip('\n').strip('\t')+"\n"
        if(len(ln)>0):
            output += "#l "+ln[0].text.split()[0]+"\n"
    return output
