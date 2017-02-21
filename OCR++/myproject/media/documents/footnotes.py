from __future__ import division
import xml.etree.ElementTree as ET
import unicodedata
import operator
import re
#import roman
import subprocess
import xml.dom.minidom

from xml.sax.saxutils import escape



directory = "/var/www/html/OCR++/myproject/media/documents/"
files=["input.xml"]


#####################

def generateXML(tree,foot_str):
    rt = tree.getroot()
    ls = rt.findall('chunk')
    st_chunk = ''
    #print("************************************")
    #print(len(ls))
    sp_length = len(ls)
    chunk_stat =0
    xroot = ET.Element("Footnotes")
    #new_footnote = ET.SubElement(xroot, "Footnotes")

    f = foot_str.split('\n')
    count = 0
    for line in f:
        cols = line.split('\t')
        #print cols
        if len(cols) == 6 and cols[5] == "FOOTNOTE":
            #print line
            st = ''
            for token in ls[count].findall('token'):
                st = st + token.text + ' '
            st = st.strip('\n')
            ET.SubElement(xroot, "footnote").text = st


        count = count +1
    return xroot

#######################





def binary(x):
    if x == "yes":
        return "1"
    return "0"


# def token_features(y):
#     x=y.strip()
#     parts=x.split('.',2)
#     pattern = re.compile('[1-9][0-9]*(\.)?([1-9][0-9]*(\.([1-9][0-9]*)?)?)?')
#     m = pattern.match(x)
#     if x=="Table" or x=="TABLE" or x=="Figure" or x=="FIGURE" or x=="Fig." or x=="FIG.":
#         return "0"
#     if m and m.span()==(0, len(x)):
#         return "1"
#     try:
#         roman.fromRoman(parts[0].upper())
#         return "1"
#     except:
#         if x[0].isupper():
#             return "2"
#         return "3"


def token_features(y):
    x=y.strip()
    if x[0].isupper():
        return "1"
    return "0"



def foot_main(root):
    #print ff
    foot_str = ''
    max_fs = 0
    p_yloc = None
    y_diff={}
    fsizes = {}

    for pages in root.findall('PAGE'):
        pre_y=0
        for texts in pages.findall('TEXT'):
            for token in texts.findall('TOKEN'):
                try:
                    #print(token.attrib)
                    fsizes[round(abs(float(token.attrib['font-size'])))]=fsizes.get(round(abs(float(token.attrib['font-size']))),0)+1
                    if(p_yloc is None):
                        p_yloc=float(token.attrib['y'])
                    if(float(token.attrib['font-size'])>max_fs):
                        max_fs=float(token.attrib['font-size'])
                    y_diff[round(abs(float(token.attrib['y'])-pre_y))]=y_diff.get(round(abs(float(token.attrib['y'])-pre_y)),0)+1
                    pre_y=float(token.attrib['y'])
                except:
                    koffe_korner = 1 #print "",#print "Oops"
    max_fs = 0
    for shit in fsizes.keys():
        #print fsizes[shit]
        if(max_fs == 0):
            max_fs = shit
            continue
        if(fsizes[shit]>fsizes[max_fs]):
            max_fs=shit
    #print max_fs
    #print("fsizes!!!")
    #print fsizes

    # exit(0)
    new_l = sorted(y_diff.iteritems(), key=operator.itemgetter(1), reverse=True)[:7]
    x_l = []
    #print(new_l)
    for k in new_l:
        if(k[0]>6.0):
            x_l.append(k)
    new_l=x_l

    x_l=[]
    mode=new_l[0][1]
    for k in new_l:
        if(not(k[1]<=mode/2 or abs(new_l[0][0]-k[0])>=4)):
            x_l.append(k)

    new_l=x_l
    #print(new_l)
    del x_l

    limit = max([x[0] for x in new_l])+2
    #print(limit)
    # exit(0)

    xroot = ET.Element("Document")
    chunk = ET.SubElement(xroot, "chunk")
    for pages in root.findall('PAGE'):
        for texts in pages.findall('TEXT'):
            for token in texts.findall('TOKEN'):
                if type(token.text) is unicode:

                    if len(token.text) == 1:
                        if ord(token.text) == 8727:
                            word = "*"
                        elif ord(token.text) == 8224:
                            word = "*"
                        elif ord(token.text) == 8225:
                            word = "*"
                        elif ord(token.text) == 167:
                            word = "*"
                        elif ord(token.text) == 958:
                            word = "*"
                        elif ord(token.text) == 182:
                            word = "*"
                        else:
                            word = unicodedata.normalize('NFKD', token.text).encode('ascii','ignore')
                        #print word
                    else:
                        if len(token.text) == 1:
                            pass #print (token.text + " " + str(ord(token.text)))
                        word = unicodedata.normalize('NFKD', token.text).encode('ascii','ignore')
                else:
                    word = token.text
                #print word
                if(word and len(word.replace(' ',''))>0):
                    if( abs(float(token.attrib['y'])-p_yloc)>=limit):
                        chunk = ET.SubElement(xroot, "chunk")
                    p_yloc = float(token.attrib['y'])
                    ET.SubElement(chunk, "token", y=token.attrib['y'], font_size=token.attrib['font-size'], bold=token.attrib['bold']).text = word

    tree = ET.ElementTree(xroot)
    #tree.write(directory+ff+"_res.xml")
    #print(tree._root)


#################################################
    #
    # newxroot = ET.Element("Document")
    # chunk = ET.SubElement(newxroot, "chunk")
    # count =0
    # p_fsize = None
    #
    # root = tree.getroot()
    #
    # for chunks in root.findall('chunk'):
    #     chunk = ET.SubElement(newxroot, "chunk")
    #     count =0
    #     stat = 0
    #     if(len(chunks)>40):stat =1
    #     for token in chunks.findall('token'):
    #         #print(token.text + " " + token.attrib["font_size"])
    #         if(p_fsize is not None and float(token.attrib["font_size"]) < p_fsize and stat==1 ):
    #             chunk = ET.SubElement(newxroot, "chunk")
    #             ET.SubElement(chunk, "token",  y=token.attrib['y'], font_size=token.attrib['font_size'], bold=token.attrib['bold']).text = token.text
    #         else:
    #             ET.SubElement(chunk, "token",  y=token.attrib['y'], font_size=token.attrib['font_size'], bold=token.attrib['bold']).text = token.text
    #             count  = count + 1
    #         p_fsize = float(token.attrib['font_size'])
    #
    # tree = ET.ElementTree(newxroot)
    # tree.write("/home/kumar_ayush/PycharmProjects/NLP/mid_train/test/softy_2/"+ff+"_fin.xml")
    #

#################################################



    newxroot = tree.getroot()

    #print ("max = "+ str(max_fs))
    #print("fsizes[max_fs] = " + str(fsizes[max_fs]))
    for achunk in newxroot.findall('chunk'):
        boldness = 0
        fsize = 0
        tcount = 0
        bool = None
        tokens = achunk.findall('token')
        if( len(tokens) == 0 ):
            #f.write("x x 0 0 0 0\n")
            foot_str += "x x 0 0 0 0\n"
            continue
        elif(len(tokens) ==1):
            tok1 = '$$$'
            tok2 = tokens[0].text
            bool = tok2
            y1 = y2 = tokens[0].attrib['y']
        else:
            tok1 = tokens[0].text
            tok2 = tokens[1].text
            size1 = tokens[0].attrib['font_size']
            size2 = tokens[1].attrib['font_size']
            y1 = tokens[0].attrib['y']
            y2 = tokens[1].attrib['y']
            bool = tok1


        tcount = len(tokens)
        for t in tokens:
            if(t.attrib['bold']=="yes"):
                boldness = boldness + 1
            fsize = fsize + float(t.attrib['font_size'])
        boldness = boldness/tcount
        fsize = (fsize/tcount)/max_fs
        #fsize = (fsize/tcount)
        if bool == "Table" or bool== "TABLE" or bool== "Figure" or bool== "FIGURE" or bool== "Fig." or bool== "FIG.":
            first_word = 1
        else:
            first_word = 0

        #if bool == "Table" or bool == "TABLE":
        #    what = "TABLE"
        #elif bool == "Figure" or bool== "FIGURE" or bool== "Fig." or bool== "FIG.":
        #    what = "FIGURE"
        #elif ((fsize*max_fs) < (max_fs/fsizes[max_fs])):
        #    what = "FOOTNOTE"

        # if (tok2[0:3] == "www" or tok2[0:4] == "http"):
        #     print(tok2)

        pattern = re.compile('[^@]+@[^@]+\.[^@]+')

        if (type(pattern.match(tok2)) == type(pattern.match('yano@k.u-tokyo.ac.jp'))):
            email = 1
            # print (email)
            # print (tok2)
        else:
            email = 0

        # pattern2 = re.compile('[a-z]\)')
        # if (type(pattern2.match(tok1)) == type(pattern.match('(a)'))):
        #     super = 1
        #     # print (email)
        #     # print (tok2)
        # else:
        #     super = 0

        #if len(tok1)>=1 and len(tok1)<=3 and (tok1.strip("()")).isalpha:
        #    super =1
            #print(super)
        #else:
        #    super =0

        if (y1>400 and (tcount >= 2) and (tok1.isdigit() or tok1 == "*" ) and (y1<y2) and  (tok2[0:3] == "www" or tok2[0:4] == "http" or tok2 == "A" or email==1 or (len(tok2)>1 and (tok2.strip(',-:;')).isalpha() and tok2[0].isupper()))):
            # print (tok2.isalpha())
            # print (tok2[0])
            what = "FOOTNOTE"
        else:
            what = "0"


        y_pos = tokens[0].attrib['y']



        #print (tok1+"\t\t\t"+tok2+"\t\t\t"+str(tcount)+"\t\t\t"+str(boldness)+"\t\t\t"+str(round(fsize,2))+"\t\t\t"+token_features(bool))
        #f.write(tok1+"\t"+tok2+"\t"+str(round(fsize,2))+"\t"+str(y_pos)+"\t"+str(first_word)+"\t"+(what)+"\n")
        foot_str += tok1+"\t"+tok2+"\t"+str(round(fsize,2))+"\t"+str(y_pos)+"\t"+str(first_word)+"\t"+(what)+"\n"

    s = generateXML(tree,foot_str)
    cc =  ET.tostring(s, 'utf-8')
    reparsed = xml.dom.minidom.parseString(cc)
    with open(directory + "FOOTNOTEop.txt",'w') as f:
        f.write(reparsed.toprettyxml(indent="\t"))

    #subprocess.call("rm " + ff + "_out.txt", shell=True)
    #subprocess.call("rm " +  ff.split('.')[0]+'_out_new.txt', shell=True)
    # subp

