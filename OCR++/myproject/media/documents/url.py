__author__ = 'kumar_ayush'

import xml.etree.ElementTree as ET
import re
import unicodedata
import operator
import roman
import subprocess
import xml.dom.minidom

directory = '/var/www/html/OCR++/myproject/media/documents/'

#files =["elsevier1.xml","elsevier2.xml","ieee1.xml","ieee2.xml","ieee3.xml","ieee_journal1.xml","ieee_journal2.xml","Springer2.xml"]
files=["input.xml"]

#####################

def generateXML(f):
    xroot = ET.Element("UniformResourceLocator")
    new_url = ET.SubElement(xroot, "URL")
    f = f.split('\n')

    count = 0
    for line in f:
        cols = line.split('\t')
        if len(cols) == 2 and cols[1] == "1":
            word = cols[0]
            st = word.strip('().,')
            ET.SubElement(new_url, "url").text = st


        count = count +1
    return xroot

#######################

def binary(x):
    if x == "yes":
        return "1"
    return "0"


def caps(y):
    x=y.strip()
    if x.islower():
        return "0"
    elif x.isupper():
        return "1"
    elif x.isdigit():
        return "2"
    elif x[:-1].isdigit():
        return "3"
    elif x[1:].islower() and x[0].isupper():
        return "4"
    else:
        return "5"




def url_main(root):
    
    #f = open(directory + ff+'.txt','w')
    f = ''

    pattern = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')


    for pages in root.findall('PAGE'):
        for texts in pages.findall('TEXT'):
            for token in texts.findall('TOKEN'):
                if type(token.text) is unicode:
                    word = unicodedata.normalize('NFKD', token.text).encode('ascii','ignore')
                else:
                    word = token.text
                    # print word


                if(word and len(word.replace(' ',''))>0):
                    #f.write((word.replace(' ','')+"\t").encode("utf-8"))
                    x = word.strip('()')
                    if(bool(pattern.match(x.replace(' ','')))):
                        #f.write((word.replace(' ','')+"\t").encode("utf-8"))
                        f += (word.replace(' ','')+"\t1\n").encode("utf-8") 
                        #f.write(("1\n").encode("utf-8"))
                    
    s = generateXML(f)
    cc =  ET.tostring(s, 'utf-8')
    reparsed = xml.dom.minidom.parseString(cc)
    with open(directory + "URLop.txt",'w') as f:
        f.write(reparsed.toprettyxml(indent="\t"))
    # subprocess.call("rm " + ff + ".txt", shell=True)
    #subprocess.call("rm " +  ff.split('.')[0]+'_out_new.txt', shell=True)
    # subp


#from subprocess import call
#f1 = open('config.txt','w')
#call(["unidecode","temp2.txt"],stdout=f1)
#f.close()
#call(["rm","temp2.txt"])