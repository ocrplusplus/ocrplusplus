import xml.etree.ElementTree as ET
import unicodedata
import time
import operator
import os

country_list = ["America", "UK", "Afghanistan", "Albania", "Algeria", "Samoa", "Andorra", "Angola", "Anguilla", "Barbuda", "Argentina", "Armenia", "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia", "Herzegowina", "Botswana", "Island", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Canada", "Cape Verde", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Costa Rica", "Ivoire", "Croatia", "Cuba", "Cyprus", "Denmark", "Djibouti", "Timor", "Ecuador", "Egypt", "Salvador", "Guinea", "Eritrea", "Estonia", "Ethiopia", "Fiji", "Finland", "France","Territories", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Gibraltar", "Greece", "Grenada", "Guadeloupe", "Guam", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Kong", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea", "Kuwait", "Kyrgyzstan", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Macau", "Macedonia", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Martinique", "Mauritania", "Mauritius", "Mayotte", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montserrat", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Caledonia", "New Zealand", "Nicaragua", "Niger", "Nigeria", "Niue", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Paraguay", "Peru", "Philippines", "Pitcairn", "Poland", "Portugal", "Rico", "Qatar", "Romania", "Russia", "Federation", "Rwanda", "Samoa", "Arabia", "Senegal", "Seychelles", "Singapore", "Slovakia", "Slovenia", "Islands", "Somalia", "South Africa", "Spain", "Lanka", "Helena", "Miquelon", "Sudan", "Suriname", "Swaziland", "Sweden", "Switzerland", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Togo", "Tokelau", "Tonga", "Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "Emirates", "Kingdom", "States", "Uruguay", "USA", "UAE", "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Yemen", "Yugoslavia", "Zambia", "Zimbabwe"]

#US_States = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Columbia", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "Hampshire", "Jersey", "York", "Carolina", "Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "Wisconsin", "Wyoming"]
US_States = []

Exceptional_names = ["MSN", "KU Leuven", "INSEAD", "ESCP Europe", "Sciences Po Paris", "ETH Zurich", "EPFL", "HKUST", "CAIDA", "BITS", "UC Berkeley", "Facebook", "Google", "Amazon", "Twitter", "MIT"]

journal_related = ["Copyright","Journal ", "JOURNAL", "ACM", "Elsevier", "ELSEVIER", "arxiv", "ARXIV", "IEEE", "ieee","Grant","GRANT","grant"]

SectionHeads = ["ABSTRACT", "INTRODUCTION", "REFERENCES"]

small_cases = ["of", "for", "and", "in", "at", "do", "a", "di", "de", "the"]

directory= '/var/www/html/OCR++/myproject/media/documents/'#raw_input()+"/"#/home/priyank/Desktop/Projects/pdfs/"
a_file = directory + "input_2.xml"

AffiliationOutputFile = "0\t0\t0\n"
titleNotOver = True

def hasAbbreviation(string):
    string = string.split(' ')
    for word in string:
        if len(word)>=3 and word.isupper():
            return True
    return False

def isAffiliation(y,fs,max_font_size):
    global titleNotOver
    x=y.strip()
    x=x.strip(',')
    if len(x) <= 1:
        return "0"
    #print x
    if fs == max_font_size and titleNotOver:            #If in Title (Biggest Font Size) it can't be affiliation.
        #print x, max_font_size, fs
        titleNotOver = False
        return "0"              #Done to prevent cases when "Research" comes in title (often)
    for Journal in journal_related:
        if x.find(Journal)!=-1:
            return "0"
    if x[1]==" " or ((not x[0].isupper()) and x[1].isupper()): #Only when there was a superscript before this line (A single character might be joint to it) =>Very IMP to prevent cases in which country name is there but not as affiliation
        for country in country_list:
            if x.find(country)!=-1:
                return "1"
    if x.find("Universit")!=-1 or x.find("Univ. ")!=-1 or x.find("Cntr. ")!=-1 or x.find("Institut")!=-1 or x.find("Department")!=-1 or x.find("Centre ")!=-1 or x.find("Center ")!=-1 or x.find("School")!=-1 or x.find(" Research")!=-1 or x.find("College")!=-1 or x.find(" Lab ")!=-1 or x.find(" Lab,")!=-1 or x.find(" Labs")!=-1 or x.find("Laborator")!=-1 or x.find("Corporat")!=-1 or x.find("Academ")!=-1 or x.find("Normale")!=-1 or x.find("Polytechnique")!=-1 or x.find("Politecnic")!=-1 or x.find("Universidad")!=-1 or x.find("Ecole")!=-1 or x.find("Inc.")!=-1 or x.find("Technologies")!=-1 or x.find("faculty")!=-1 or x.find("Dept.")!=-1 or x in Exceptional_names:# or hasAbbreviation(x):
        return "1"
    return "0"


def isEmail(y):
    x=y.strip()
    x = x.strip('.')
    isatr = 0
    for i in range(len(x)):
        if x[i] == "@":
            isatr = 1
        if((isatr==1) and (x[i]==".") and (x[i+1]<"z" and x[i+1]>"a")):
            return "1"
    return "0"



def FindAffiliation(block,fs,max_font_size):
    global AffiliationOutputFile
    ret = "0"
    #block = block.replace(',','#$#')
    t = block.split('#$#')
    aff = "0"
    flag = False
    for j in t:
        j = j.strip()
        p = isAffiliation(j,fs,max_font_size)
        if p=="1":
            ret = "1"
        if p == "1" or aff == "1":
            aff = "1"
            x = j.split(' ')
            for i in x:
                i = i.strip(".").strip(",")
                if len(i)>0:
                    if isEmail(i) == "1":
                        aff = "0"
                        # AffiliationOutputFile.write("0\t0\t0\n")
                        AffiliationOutputFile = AffiliationOutputFile + "0\t0\t0\n"
                    else:
                        # AffiliationOutputFile.write((i+"\t").encode("utf-8"))
                        # AffiliationOutputFile.write(("1\t").encode("utf-8"))
                        # AffiliationOutputFile.write(("0\n").encode("utf-8"))
                        AffiliationOutputFile = AffiliationOutputFile + (i+"\t").encode("utf-8")
                        AffiliationOutputFile = AffiliationOutputFile + ("1\t").encode("utf-8")
                        AffiliationOutputFile = AffiliationOutputFile + ("0\n").encode("utf-8")
                    if p == "0" and (i.replace(".","") in country_list or i in US_States):
                        aff = "0"
                        # AffiliationOutputFile.write("0\t0\t0\n")
                        AffiliationOutputFile = AffiliationOutputFile + "0\t0\t0\n"
    return ret


def cutShort(stri):
    cutBefore = stri.find(" with")
    if cutBefore!=-1:
        stri = stri[cutBefore+6:]
    stri = stri.strip()
    striList = stri.split(' ')
    finalStrList = ""
    for word in striList:
        if (word.upper().find("EMAIL")==-1 and word.upper().find("E-MAIL")==-1) and (word[0].isupper() or (len(word)>1 and word[0]>='0' and word[0]<='9') or word in small_cases):
            finalStrList += word + " "
    i=0
    try:
        while not finalStrList[i].isupper():
            i+=1
    except:
        finalStrList = ""
    finalStrList = finalStrList[i:]
    return finalStrList.strip()






def aff_main(xroot, max_font_size):
    global AffiliationOutputFile
    stringforAff = ""
    count = 0
    fs = 0
    cnt = 0
    boldness = "no"
    prev_size = 0
    fontSize = 0
    skipThis = False
    THRESHHOLD_FOR_BODY = 1800
    min_result_ys = 700 #Hold value of minimum y (topmost) where there is an affiliation so that if found above, we do not check in the footnotes
    for achunk in xroot.findall('chunk'):
        stringforAff = ""
        cnt = 0
        pre_y = 0
        AllTokens = achunk.findall('token')
        if AllTokens[0].attrib['page_number'] == "3":
            break
        if fontSize == AllTokens[0].attrib['font_size']:    #Still in body
            skipThis = False
            continue
        if len(AllTokens)<=2 and (AllTokens[0].text.upper() in SectionHeads or (len(AllTokens)>1 and AllTokens[1].text.upper() in SectionHeads)):#or AllTokens[0].attrib['bold']=="yes"):
            skipThis = True #Section Heading... Body starts from next line
            continue
        if skipThis:    #Body Starts... Record the font size of this body
            fontSize = AllTokens[0].attrib["font_size"]
            #print fontSize, AllTokens[0].text
            skipThis = False
            continue
        for tokens in AllTokens:
            
            if tokens is None or tokens.text is None:
                continue
            if float(tokens.attrib['y']) - min_result_ys >=300:    #We Found result above and this is footnote => Don't consider this block, go to the next one
                break

            prev_size = tokens.attrib['font_size']
            if pre_y == 0:
                pre_y = tokens.attrib['y']
            elif pre_y != tokens.attrib['y']:
                if pre_y < tokens.attrib['y']:
                    if float(tokens.attrib['y']) - float(pre_y) < float(prev_size)/2:       #Encounter a SuperScript => New aff starts in case it is aff. 
                        if(FindAffiliation(stringforAff.replace("- #$#",""),fs,max_font_size)=="1"):
                            if min_result_ys>float(tokens.attrib['y']):
                                min_result_ys = float(tokens.attrib['y'])
                        # AffiliationOutputFile.write("0\t0\t0\n")
                        AffiliationOutputFile = AffiliationOutputFile + "0\t0\t0\n"
                        stringforAff = stringforAff[-2:]
                    else:
                        stringforAff += "#$#"

                else:
                    if(FindAffiliation(stringforAff.replace("- #$#",""),fs,max_font_size)=="1"):
                        if min_result_ys>float(tokens.attrib['y']):
                            min_result_ys = float(tokens.attrib['y'])
                    # AffiliationOutputFile.write("0\t0\t0\n")
                    AffiliationOutputFile = AffiliationOutputFile + "0\t0\t0\n"
                    stringforAff = ""
                pre_y = tokens.attrib['y']
            else:
                pass


            if type(tokens.text) is unicode:
                tokens.text = unicodedata.normalize('NFKD', tokens.text).encode('ascii','ignore')
            elif type(tokens.text) is str:
                tokens.text = tokens.text
            else:
                print type(tokens.text)

            stringforAff += tokens.text + " "
            try:
                fs = float(tokens.attrib['font_size'])
            except:
                pass
            cnt += 1
        
        if cnt > THRESHHOLD_FOR_BODY:
            continue
        if(FindAffiliation(stringforAff.replace("- #$#",""),fs,max_font_size)=="1"):
            if min_result_ys>float(tokens.attrib['y']):
                min_result_ys = float(tokens.attrib['y'])
                        
        # AffiliationOutputFile.write("0\t0\t0\n")
        AffiliationOutputFile = AffiliationOutputFile + "0\t0\t0\n"

    #############################################################################################################################

    #print AffiliationOutputFile
    w_flag = "0"   # to check if a Affiliation is already going on
    # directory= ''#raw_input()+"/"#/home/priyank/Desktop/Projects/pdfs/"
    # filetoread = directory + "input_parse.txt"
    filetoread = AffiliationOutputFile

    
    '''
    inp_allaff_str = ''
    #outfile.write("<" + (filetoread.split(".")[0]).split("/")[-1] + ">\n")
    # with open(filetoread,'r') as f:
    stri = ""
    lines = filetoread.split('\n')
    for line in lines:
        abc = line.split()

        if len(abc) >= 1:  # if not a blank line

            if abc[1] == "1":   #output column
                if w_flag == "0":  #if start of Affiliation
                    #outfile.write("\n\t<Affiliation>\n\t\t")
                    inp_allaff_str += "\n\t<Affiliation>\n\t\t"
                stri += ((abc[0].strip(',')).strip('.') + ' ')
                w_flag = "1"
            else:
                if w_flag == "1":
                    stri = cutShort(stri)
                    if stri.find(" ")==-1 and stri.isupper()==False: #Only one word which isn't an abbreviation => Can't be an affiliation [Note: May fail in cases like "Facebook", "Google", "Amazon" etc]
                        #outfile.seek(-18,os.SEEK_END)
                        #outfile.truncate()
                        inp_allaff_str = inp_allaff_str[:-18]
                    elif stri.isdigit() and len(stri)>=5:
                        #outfile.seek(-35,os.SEEK_END)
                        #outfile.truncate()
                        inp_allaff_str = inp_allaff_str[:-35]
                        #outfile.write(" " + stri)
                        inp_allaff_str += " " + stri
                        #outfile.write("\n\t</Affiliation>\n")
                        inp_allaff_str += "\n\t</Affiliation>\n"
                    else:
                        #outfile.write(stri)
                        inp_allaff_str += stri
                        #outfile.write("\n\t</Affiliation>\n")
                        inp_allaff_str += "\n\t</Affiliation>\n"
                    w_flag = "0"
                    stri = ""
    outfile = open(directory + "input_AllAffiliations.txt",'w')
    outfile.write(inp_allaff_str)
    outfile.close()  
    return inp_allaff_str  
    '''
    root =  ET.Element("Affiliations")
    currentElem = ET.Element("IgnoreThis___NeverUSed")
    tree = ET.ElementTree(root)
    lines = filetoread.split('\n')
    stri = ""
    for line in lines:
        abc = line.split()

        if len(abc) >= 1:  # if not a blank line

            if abc[1] == "1":   #output column
                if w_flag == "0":  #if start of Affiliation
                    prevElem = currentElem
                    currentElem = ET.SubElement(root, "Affiliation")
                    #outfile.write("\n\t<Affiliation>\n\t\t")
                    # inp_allaff_str += "\n\t<Affiliation>\n\t\t"
                stri += ((abc[0].strip(',')).strip('.') + ' ')
                currentElem.text = ''
                # currentElem.text = ((abc[0].strip(',')).strip('.') + ' ')
                w_flag = "1"
            else:
                if w_flag == "1":
                    stri = cutShort(stri)
                    if stri.find(" ")==-1 and stri.isupper()==False: #Only one word which isn't an abbreviation => Can't be an affiliation [Note: May fail in cases like "Facebook", "Google", "Amazon" etc]
                        root.remove(currentElem)
                        currentElem = prevElem
                        # inp_allaff_str = inp_allaff_str[:-18]
                    elif stri.isdigit() and len(stri)>=5:
                        #inp_allaff_str = inp_allaff_str[:-35]
                        prevElem.text += " "+stri;
                        root.remove(currentElem)
                        currentElem = prevElem
                        #inp_allaff_str += " " + stri
                        #inp_allaff_str += "\n\t</Affiliation>\n"
                    else:
                        # inp_allaff_str += stri
                        # inp_allaff_str += "\n\t</Affiliation>\n"
                        currentElem.text+=stri
                    w_flag = "0"
                    stri = ""

    tree.write(directory + 'input_AllAffiliations.txt')
    # print ET.tostring(root,method='xml')
    return root
    
