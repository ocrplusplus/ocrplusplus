import os

directory = "/var/www/html/OCR++/myproject/media/documents/"

import subprocess
import threading
from subprocess import Popen, PIPE
import Aff_new
import Email_new
import TitleAuthor_parse
import chunk
import operator
import glob
import xml.etree.ElementTree as ET
import Secmapping
import printAuthor
import printnameformap
import authorEmailMapping
import cit_final
import footnotes
import tables_figures
import url
import generate_xml
# import xmlParsing
# import testFoldedData
# import genrateCoraxml
import time

def runScript():

    copyTime = 0
    pdftoxmltime = 0
    parseTime = 0
    footnotestime = 0
    tables_figures_time = 0
    urltime = 0
    cit2reftime = 0
    chunk1time = 0
    chunk2time = 0
    secMapTime = 0
    emailTime = 0
    affTime = 0
    titleTime = 0
    authorTime = 0
    mappingtime = 0
    xmlParsingTime = 0
    testFoldedDataTime = 0
    genrateCoraxmlTime = 0

    #print os.getcwd()
    os.chdir(directory)
    #print os.getcwd()

    #subprocess.call(directory + "./Clear.sh",shell=True)
    # print paperid
    file_name = glob.glob(directory+'*.pdf')
    #print "main_script_batch : ", file_name
    srno = 1
    for fname in file_name:
        #print srno
        srno = srno+1
        # subprocess.call("rm " + directory + "input.pdf", shell=True)
        fn = fname.split('/')
        fn = fn[-1]
        #print fn
        # subprocess.call("clear", shell=True)
        startTime = time.time()
        # subprocess.call("cp " + directory + "testpdfs/" + fn + " " + directory + "input.pdf", shell=True)
        # copyTime += time.time()-startTime
        startTime = time.time()
        #print "Hello 1"
        subprocess.call(directory + "pdftoxml.linux64.exe.1.2_7 -noImage -noImageInline " + directory + "input.pdf "+directory + "input.xml", shell=True)
        #print "Hello 2"
        pdftoxmltime += time.time()-startTime
        #subprocess.call("./Clear.sh", shell=True)
        #subprocess.call(directory + "./IntegratedShellScript.sh ", shell=True)
        try:
            a_file = directory + "input.xml"
            #print "Hello 3"

            startTime = time.time()
            tree = ET.parse(a_file)
            root = tree.getroot()
            parseTime += time.time()-startTime

            startTime = time.time()
            footnotes.foot_main(root)
            footnotestime += time.time()-startTime

            startTime = time.time()
            tables_figures.tab_fig_main(root)
            tables_figures_time += time.time()-startTime

            startTime = time.time()
            url.url_main(root)
            urltime += time.time()-startTime

            startTime = time.time()
            References_list = cit_final.mainf(root)
            cit2reftime += time.time()-startTime
            
        except Exception, inst:
            print "Exception : In main"
            #print e
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args
            print inst           # __str__ allows args to be printed directly
        
        try:
            startTime = time.time()
            chunked_root_1, modalFS = chunk.chunk_1(root)
            chunk1time += time.time()-startTime
        except Exception, inst:
            print "Exception : In chunk1"
            #print e
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args
            print inst           # __str__ allows args to be printed directly
        
        try:
            startTime = time.time()
            chunked_root_2, max_font_size = chunk.chunk_2(chunked_root_1)
            chunk2time += time.time()-startTime
        except Exception, inst:
            print "Exception : In chunk2"
            #print e
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args
            print inst           # __str__ allows args to be printed directly
        
        try:
            startTime = time.time()
            Secmapping.sec_main(chunked_root_1, chunked_root_2, modalFS)
            secMapTime += time.time()-startTime
        except Exception, inst:
            print "Exception : In Sections"
            #print e
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args
            print inst           # __str__ allows args to be printed directly
        

        try:
            startTime = time.time()
            Email_new.foutMail = "0\t0\t0\n"
            email_str_for_Map = Email_new.Email_main(root)
            emailTime += time.time()-startTime
        except Exception, inst:
            print "Exception : In Email"
            #print e
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args
            print inst           # __str__ allows args to be printed directly
        
        try:
            startTime = time.time()
            Aff_new.titleNotOver = True
            Aff_new.AffiliationOutputFile = "0\t0\t0\n"
            aff_xml = Aff_new.aff_main(chunked_root_1,max_font_size)
            affTime += time.time()-startTime
        except Exception, inst:
            print "Exception : In Affiliation"
            #print e
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args
            print inst           # __str__ allows args to be printed directly
        

        try:
            startTime = time.time()
            title_str = TitleAuthor_parse.TitleAuthor_parse(root,aff_xml)
            titleTime += time.time()-startTime
        except Exception, inst:
            print "Exception : In Title"
            #print e
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args
            print inst           # __str__ allows args to be printed directly
        
        #print "Generating Title Author xml"
        try:
            startTime = time.time()
            title_author_xml = printAuthor.printAuthor(title_str,aff_xml)
            authorTime += time.time()-startTime
        except Exception, inst:
            print "Exception : In Author"
            #print e
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args
            print inst           # __str__ allows args to be printed directly
        
        #print "Got title_author_xml"
        try:
           startTime = time.time()
           name_for_map = printnameformap.genAuthorFileForMap(title_author_xml)
           authorEmailMapping.authorEmailMap(name_for_map,email_str_for_Map)         
           mappingtime += time.time()-startTime
        except Exception, inst:
           print "Exception : In Email_Author_Matching"
           #print e
           print type(inst)     # the exception instance
           print inst.args      # arguments stored in .args
           print inst           # __str__ allows args to be printed directly

        try:
            xml = generate_xml.main()
        except Exception, inst:
            print "Exception : In XML generation"
            #print e
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args
            print inst           # __str__ allows args to be printed directly
        
        # try:
        #     startTime = time.time()
        #     xmlParsing.main(root,max_font_size,References_list)
        #     xmlParsingTime += time.time()-startTime

        #     startTime = time.time()
        #     testFoldedData.testFoldedData()
        #     testFoldedDataTime += time.time()-startTime

        #     startTime = time.time()
        #     genrateCoraxml.main()
        #     genrateCoraxmlTime += time.time()-startTime

        # except Exception, inst:
        #     print "Exception : In Manvi's code"
        #     #print e
        #     print type(inst)     # the exception instance
        #     print inst.args      # arguments stored in .args
        #     print inst           # __str__ allows args to be printed directly
        
    subprocess.call("./eval_op.sh", shell=True)
    #print "copyTime = " + str(copyTime)
    #print "pdftoxmltime = " + str(pdftoxmltime)
    #print "parseTime = " + str(parseTime)
    #print "footnotestime = " + str(footnotestime)
    #print "tables_figures_time = " + str(tables_figures_time)
    #print "urltime = " + str(urltime)
    #print "cit2reftime = " + str(cit2reftime)
    #print "chunk1time = " + str(chunk1time)
    #print "chunk2time = " + str(chunk2time)
    #print "secMapTime = " + str(secMapTime)
    #print "emailTime = " + str(emailTime)
    #print "affTime = " + str(affTime)
    #print "titleTime = " + str(titleTime)
    #print "authorTime = " + str(authorTime)
    #print "mappingtime = " + str(mappingtime)
    # #print "xmlParsingTime = " + str(xmlParsingTime)
    # print "testFoldedDataTime = " + str(testFoldedDataTime)
    # print "genrateCoraxmlTime = " + str(genrateCoraxmlTime)
        
        # ftit = open(directory + "all_title.txt",'a')
        # faut = open(directory + "all_authors.txt",'a')
        # fsec = open(directory + "all_sec.txt",'a')
        # furl = open(directory + "all_url.txt",'a')
        # ffoot = open(directory + "all_foot.txt",'a')    
        # femail = open(directory + "all_email.txt",'a')
        # faffil = open(directory + "all_affil.txt",'a')
        # fmap = open(directory + "all_map.txt",'a')
        # ftabfig = open(directory + "all_tabfig.txt",'a')
        # ftit.write("\n"+fn+".xml\n")
        # faut.write("\n"+fn+".xml\n")
        # fsec.write("\n"+fn+".xml\n")
        # furl.write("\n"+fn+".xml\n")
        # ffoot.write("\n"+fn+".xml\n")
        # femail.write("\n"+fn+".xml\n")
        # faffil.write("\n"+fn+".xml\n")
        # fmap.write("\n"+fn+".xml\n")
        # ftabfig.write("\n"+fn+".xml\n")

        # ftit.close()
        # faut.close()
        # fsec.close()
        # furl.close()
        # ffoot.close()
        # faut.close()
        # femail.close()
        # faffil.close()
        # fmap.close()
        # ftabfig.close()
        # subprocess.call(directory + "./Add_append.sh",shell=True)

runScript()
