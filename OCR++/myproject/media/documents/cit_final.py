from __future__ import division
import xml.etree.ElementTree as ET
import unicodedata
import re
import os
import string
import sys
import types
import copy

root_folder = ''

def binary(x):
    if x == "yes":
        return "1"
    return "0"


def search_name_year_in_references(Reference,name,year):
    name = name.replace(" ","")
    for i in range(len(Reference)):
        refs = Reference[i]
        if name in refs and year in refs:
            return i
    return -1                                  

def search_doublename_in_references(Reference,name1,name2,year):
    name1 = name1.replace(" ","")
    name2 = name2.replace(" ","")
    for i in range(len(Reference)):
        refs = Reference[i]
        if name1 in refs and name2 in refs and year in refs:
            return i
    return -1                               

def mainf(root):
    directory = "/var/www/html/OCR++/myproject/media/documents/"
    doc_Sam = ET.Element("Document")
    refs_Sam = ET.SubElement(doc_Sam, "References")
    cit2ref_Sam = ET.SubElement(doc_Sam, "Cit2ref")
    count = 0
    
    flag_in_reference_section = False
    Reference = []

    for pages in root.findall('PAGE'):
        texts = pages.findall('TEXT')
        for i  in range(len(texts)):
            tokens = texts[i].findall('TOKEN')
            if flag_in_reference_section==False:
                for j in range(len(tokens)):

                    if type(tokens[j].text) is unicode:
                        word = unicodedata.normalize('NFKD', tokens[j].text).encode('ascii','ignore')
                    else:
                        word = tokens[j].text
                        if isinstance(word, types.NoneType):
                            continue

                    if(len(word.replace(' ',''))>0):
                        if ((word=="REFERENCES" or word=="References") and binary(tokens[j].attrib['bold'])):
                            flag_in_reference_section = True
                            flag_first_token_in_reference_section = True
                            continue
            else:
                current_x = texts[i].attrib['x']
                current_y = texts[i].attrib['y']
                try:
                    current_size = float(tokens[0].attrib['font-size'])
                except:
                    current_size = 0
                try:
                    current_font = tokens[0].attrib['font-name']
                except:
                    current_font = ""
                current_font = current_font.lower()
                current_bold = tokens[0].attrib['bold']
                current_italic = tokens[0].attrib['italic']

                if flag_first_token_in_reference_section:  
                    first_token_x = current_x
                    index = 0
                    Reference.append("")
                    first_line_gap = float(texts[i+1].attrib['y']) - float(current_y)
                    try:
                        first_size = float(tokens[0].attrib['font-size'])
                    except:
                        first_size = 0
                    try:
                        first_font = tokens[0].attrib['font-name'].lower()
                    except:
                        first_font = ""
                    first_lower = first_font.lower()
                    try:
                        first_bold = tokens[0].attrib['bold']
                    except:
                        first_bold = False
                    try:
                        first_italic = tokens[0].attrib['italic']
                    except:
                        first_italic = False
                    flag_first_token_in_reference_section = False
                else:
                    if (float(current_y) < float(previous_y)):  
                        if current_size < first_size - 0.1 or current_size > first_size + 0.1 or current_font != first_font or current_bold != first_bold or current_italic != first_italic: #not a 
                            continue
                        k = i + 1 
                        while(True):
                            if k >= len(texts):     
                                first_token_x = current_x
                                break
                            next_x = texts[k].attrib['x']
                            if(float(next_x) > float(current_x) + 0.1):
                                first_token_x = current_x
                                index = index + 1
                                Reference.append("")
                                break
                            if(float(next_x) < float(current_x) - 0.1): 
                                first_token_x = next_x
                                break
                            k = k + 1
                    else:
                        if float(current_y) - float(previous_y) > 3 * first_line_gap:
                            continue
                        if (float(current_x) < float(first_token_x) + 0.1 ):
                            index = index + 1
                            Reference.append("")

                previous_x = current_x
                previous_y = current_y

                for j in range(len(tokens)):

                    if type(tokens[j].text) is unicode:
                        word = unicodedata.normalize('NFKD', tokens[j].text).encode('ascii','ignore')
                    else:
                        word = tokens[j].text
                        if isinstance(word, types.NoneType):
                            continue
                    if(len(word.replace(' ',''))>0):
                        word = word.replace('&','%27')
                        Reference[index] += word
                        Reference[index] += " "


    citations_no = 0
    flag_not_in_reference_section = True
    two_lines = ""
    flag_hyphen = False
    max_ref_id = -1

    for pages in root.findall('PAGE'):
        count+=1
        texts = pages.findall('TEXT')
        for i  in range(len(texts)):
            flag_hyphen = False
            if i:
                if line.endswith("-"):
                    line = line[:-1]
                    flag_hyphen = True
                two_lines = line
            line = ""
            tokens = texts[i].findall('TOKEN')
            for j in range(len(tokens)):
                if type(tokens[j].text) is unicode:
                    word = unicodedata.normalize('NFKD', tokens[j].text).encode('ascii','ignore')
                else:
                    word = tokens[j].text
                    if isinstance(word, types.NoneType):
                        continue
                    if (len(word)>0) and flag_not_in_reference_section==True:
                        if ((word=="REFERENCES" or word=="References") and binary(tokens[j].attrib['bold'])):
                            flag_not_in_reference_section = False
                        word += " "
                        line += word
            if flag_hyphen:
                line = line[1:]
            two_lines += line


            if flag_not_in_reference_section==True:
                regex = re.compile("([A-Z][a-zA-Z]* et al[.] \[(\d{1,3})\])")
                result = re.findall(regex, two_lines)
                if len(result) > 0:
                    for a in result:
                        if (int(a[1])-1) >= 0 and int(a[1]) <= len(Reference) :
                            citations_no += 1
                            two_lines = two_lines.replace(a[0],'CITATION')
                            line = line.replace(a[0],'CITATION')
                            if int(a[1])-1 > max_ref_id:
                                max_ref_id = int(a[1])-1
                            ET.SubElement(cit2ref_Sam, "cit2ref", ref_id=str(a[1]), reference=Reference[int(a[1])-1]).text = a[0]



                regex = re.compile("([A-Z][a-zA-Z]* \[(\d{2})\])")
                result = re.findall(regex, two_lines)
                if len(result) > 0:
                    for a in result:
                        if (int(a[1])-1) >= 0 and int(a[1]) <= len(Reference) :
                            citations_no += 1
                            two_lines = two_lines.replace(a[0],'CITATION')
                            line = line.replace(a[0],'CITATION')
                            if int(a[1])-1 > max_ref_id:
                                max_ref_id = int(a[1])-1
                            ET.SubElement(cit2ref_Sam, "cit2ref", ref_id=str(a[1]), reference=Reference[int(a[1])-1]).text = a[0]

                regex = re.compile("([A-Z][a-zA-Z]* et al[.][ ]*\[(\d{1})\])")
                result = re.findall(regex, two_lines)
                if len(result) > 0:
                    for a in result:
                        if (int(a[1])-1) >= 0 and int(a[1]) <= len(Reference) :
                            citations_no += 1
                            two_lines = two_lines.replace(a[0],'CITATION')
                            line = line.replace(a[0],'CITATION')
                            if int(a[1])-1 > max_ref_id:
                                max_ref_id = int(a[1])-1
                            ET.SubElement(cit2ref_Sam, "cit2ref",  ref_id=str(a[1]), reference=Reference[int(a[1])-1]).text = a[0]

                regex = re.compile("(([A-Z][a-zA-Z]*) et al[.][,] (\d{4}[a-z]))")
                result = re.findall(regex, two_lines)
                if len(result) > 0:
                    for a in result:
                        citations_no += 1
                        two_lines = two_lines.replace(a[0],'CITATION')
                        line = line.replace(a[0],'CITATION')
                        r_id = search_name_year_in_references(Reference,a[1],a[2])
                        if(r_id >= 0):
                            if r_id > max_ref_id:
                                max_ref_id = r_id
                            ET.SubElement(cit2ref_Sam, "cit2ref",  ref_id=str(r_id+1), reference=Reference[r_id]).text = a[0]

                regex = re.compile("(([A-Z][a-zA-Z]*) et al[.][,] (\d{4}))")
                result = re.findall(regex, two_lines)
                if len(result) > 0:
                    for a in result:
                        citations_no += 1
                        two_lines = two_lines.replace(a[0],'CITATION')
                        line = line.replace(a[0],'CITATION')
                        r_id = search_name_year_in_references(Reference,a[1],a[2])
                        if(r_id >= 0):
                            if r_id > max_ref_id:
                                max_ref_id = r_id
                            ET.SubElement(cit2ref_Sam, "cit2ref", ref_id=str(r_id+1),reference=Reference[r_id]).text = a[0]


                regex = re.compile("(([A-Z][a-zA-Z]*) et al[.][,] \((\d{4})\))")
                result = re.findall(regex, two_lines)
                if len(result) > 0:
                    for a in result:
                        citations_no += 1
                        two_lines = two_lines.replace(a[0],'CITATION')
                        line = line.replace(a[0],'CITATION')
                        r_id = search_name_year_in_references(Reference,a[1],a[2])
                        if(r_id >= 0):
                            if r_id > max_ref_id:
                                max_ref_id = r_id
                            ET.SubElement(cit2ref_Sam, "cit2ref", ref_id=str(r_id+1),reference=Reference[r_id]).text = a[0]

                regex = re.compile("(([A-Z][a-zA-Z]*) et al[.] (\d{4}))")
                result = re.findall(regex, two_lines)
                if len(result) > 0:
                    for a in result:
                        citations_no += 1
                        two_lines = two_lines.replace(a[0],'CITATION')
                        line = line.replace(a[0],'CITATION')
                        r_id = search_name_year_in_references(Reference,a[1],a[2])
                        if(r_id >= 0):
                            if r_id > max_ref_id:
                                max_ref_id = r_id
                            ET.SubElement(cit2ref_Sam, "cit2ref",ref_id=str(r_id+1), reference=Reference[r_id]).text = a[0]

                regex = re.compile("(([A-Z][a-zA-Z]*) et al[.] \((\d{4})\))")
                result = re.findall(regex, two_lines)
                if len(result) > 0:
                    for a in result:
                        citations_no += 1
                        two_lines = two_lines.replace(a[0],'CITATION')
                        line = line.replace(a[0],'CITATION')
                        r_id = search_name_year_in_references(Reference,a[1],a[2])
                        if(r_id >= 0):
                            if r_id > max_ref_id:
                                max_ref_id = r_id
                            ET.SubElement(cit2ref_Sam, "cit2ref", ref_id=str(r_id+1),reference=Reference[r_id]).text = a[0]

                regex = re.compile("(([A-Z][a-zA-Z]*) and ([A-Z][a-zA-Z]*) \((\d{4})\))")
                result = re.findall(regex, two_lines)
                if len(result) > 0:
                    for a in result:
                        citations_no += 1
                        two_lines = two_lines.replace(a[0],'CITATION')
                        line = line.replace(a[1],'CITATION')
                        r_id = search_doublename_in_references(Reference,a[1],a[2],a[3])
                        if(r_id >= 0):
                            if r_id > max_ref_id:
                                max_ref_id = r_id
                            ET.SubElement(cit2ref_Sam, "cit2ref", ref_id=str(r_id+1),reference=Reference[r_id]).text = a[0]

                regex = re.compile("(([A-Z][a-zA-Z]*) [&] ([A-Z][a-zA-Z]*) \((\d{4})\))")
                result = re.findall(regex, two_lines)
                if len(result) > 0:
                    for a in result:
                        citations_no += 1
                        two_lines = two_lines.replace(a[0],'CITATION')
                        line = line.replace(a[1],'CITATION')
                        r_id = search_doublename_in_references(Reference,a[1],a[2],a[3])
                        if(r_id >= 0):
                            if r_id > max_ref_id:
                                max_ref_id = r_id
                            ET.SubElement(cit2ref_Sam, "cit2ref", ref_id=str(r_id+1),reference=Reference[r_id]).text = a[0]

                regex = re.compile("(([A-Z][a-zA-Z]*) and ([A-Z][a-zA-Z]*)[,] (\d{4}))")
                result = re.findall(regex, two_lines)
                if len(result) > 0:
                    for a in result:
                        citations_no += 1
                        two_lines = two_lines.replace(a[0],'CITATION')
                        line = line.replace(a[1],'CITATION')
                        r_id = search_doublename_in_references(Reference,a[1],a[2],a[3])
                        if(r_id >= 0):
                            if r_id > max_ref_id:
                                max_ref_id = r_id
                            ET.SubElement(cit2ref_Sam, "cit2ref", ref_id=str(r_id+1),reference=Reference[r_id]).text = a[0]

                regex = re.compile("(([A-Z][a-zA-Z]*) [&] ([A-Z][a-zA-Z]*)[,] (\d{4}))")
                result = re.findall(regex, two_lines)
                if len(result) > 0:
                    for a in result:
                        citations_no += 1
                        two_lines = two_lines.replace(a[0],'CITATION')
                        line = line.replace(a[1],'CITATION')
                        r_id = search_doublename_in_references(Reference,a[1],a[2],a[3])
                        if(r_id >= 0):
                            if r_id > max_ref_id:
                                max_ref_id = r_id
                            ET.SubElement(cit2ref_Sam, "cit2ref", ref_id=str(r_id+1),reference=Reference[r_id]).text = a[0]

                regex = re.compile("(([A-Z][a-zA-Z]*)[,] (\d{4}))")
                result = re.findall(regex, two_lines)
                if len(result) > 0:
                    for a in result:
                        citations_no += 1
                        two_lines = two_lines.replace(a[0],'CITATION')
                        line = line.replace(a[0],'CITATION')
                        r_id = search_name_year_in_references(Reference,a[1],a[2])
                        if(r_id >= 0):
                            if r_id > max_ref_id:
                                max_ref_id = r_id
                            ET.SubElement(cit2ref_Sam, "cit2ref", ref_id=str(r_id+1),reference=Reference[r_id]).text = a[0]

                regex = re.compile("(([A-Z][a-zA-Z]*) (\d{4}))")
                result = re.findall(regex, two_lines)
                if len(result) > 0:
                    for a in result:
                        citations_no += 1
                        two_lines = two_lines.replace(a[0],'CITATION')
                        line = line.replace(a[0],'CITATION')
                        r_id = search_name_year_in_references(Reference,a[1],a[2])
                        if(r_id >= 0):
                            if r_id > max_ref_id:
                                max_ref_id = r_id
                            ET.SubElement(cit2ref_Sam, "cit2ref", ref_id=str(r_id+1),reference=Reference[r_id]).text = a[0]

                regex = re.compile("(([A-Z][a-zA-Z]*) \((\d{4}[a-z]*)\))")
                result = re.findall(regex, two_lines)
                if len(result) > 0:
                    for a in result:
                        citations_no += 1
                        two_lines = two_lines.replace(a[0],'CITATION')
                        line = line.replace(a[0],'CITATION')
                        r_id = search_name_year_in_references(Reference,a[1],a[2])
                        if(r_id >= 0):
                            if r_id > max_ref_id:
                                max_ref_id = r_id
                            ET.SubElement(cit2ref_Sam, "cit2ref", ref_id=str(r_id+1),reference=Reference[r_id]).text = a[0]

                regex = re.compile("(.*?\((.*?)\))")
                result = re.findall(regex, two_lines)
                if len(result) > 0:
                        for a in result:
                            citations_no += 1
                            temp = a[0]
                            regex1 = re.compile("\d{4}$")
                            cits = a[1].split(';')
                            for citation in cits:
                                citation = citation.replace(" ","")
                                if regex1.match(citation) and (int(citation)-1) >= 0 and int(citation) <= len(Reference) :
                                    temp = temp.replace(citation,'CITATION')
                        two_lines = two_lines.replace(a[0],temp)
                        line = line.replace(a[0],'CITATION')

                regex = re.compile("(.*?\[(.*?)\])")
                result = re.findall(regex, two_lines)
                if len(result) > 0:
                    for a in result:
                        citations_no += 1
                        temp = a[0]
                        regex1 = re.compile("\d{1,3}$")
                        cits = a[1].split(',')
                        for citation in cits:
                            citation = citation.replace(" ","")
                            if regex1.match(citation) and (int(citation)-1) >= 0 and int(citation) <= len(Reference) :
                                line = line.replace(citation,'CITATION',1)
                                ET.SubElement(cit2ref_Sam, "cit2ref", ref_id=str(citation), reference=Reference[int(citation)-1]).text = a[0]
                                if int(citation)-1 > max_ref_id:
                                    max_ref_id = int(citation)-1

    # cit2ref.write("<!-- REFERENCES -->\n")
    for i in range(max_ref_id + 1):
        ET.SubElement(refs_Sam, "Reference", id=str(i+1)).text = Reference[i]
    ###########################################

    # cit2ref.write("<!-- END DOC -->\n")
    ET.ElementTree(doc_Sam).write(directory + "input_res.xml")
    return Reference
