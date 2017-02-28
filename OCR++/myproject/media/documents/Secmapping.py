
from __future__ import division

import xml.etree.ElementTree as ET
import unicodedata
import operator
import itertools as iter

import subprocess
import xml.dom.minidom

import roman
import math

directory = '/var/www/html/OCR++/myproject/media/documents/'

"""
Create an XML of headings and sections for indexed inputs
"""
def generateXML(tree):
	root = tree.getroot()
	chunk_list = root.findall('chunk')
	st_chunk = ''
	chunk_list_length = len(chunk_list)
	chunk_stat =0
	xroot = ET.Element("sec_map")
	new_section = ET.SubElement(xroot, "section")
	with open(directory + "finalsec.txt", "r") as f:
		count = 0
		for line in f:
			cols = line.split('\t')
			if len(cols)==9 and cols[8] == '1\n':
				st = ''
				for token in chunk_list[count].findall('token'):
					st = st + token.text+' '
				st = st.strip('\n')
				if(chunk_stat == 1):
					ET.SubElement(new_section, "chunk").text = st_chunk
					chunk_stat = 0
					st_chunk = ''
				new_section = ET.SubElement(xroot, "section")
				ET.SubElement(new_section, "heading").text = st
			elif(count<chunk_list_length) :
				chunk_stat =1
				for token in chunk_list[count].findall('token'):
					st_chunk = st_chunk + token.text+' '
				st_chunk = st_chunk.strip('\n')
			count = count + 1
	if chunk_stat == 1:
		 ET.SubElement(new_section, "chunk").text = st_chunk
	return xroot


"""
Create an XML of headings and sections for non-indexed inputs
"""

def generateXML_NI(tree):
	root = tree.getroot()
	chunk_list = root.findall('chunk')
	st_chunk = ''
	chunk_list_length = len(chunk_list)
	chunk_stat =0
	xroot = ET.Element("sec_map")
	new_section = ET.SubElement(xroot, "section")
	with open(directory + "finalsec_NI.txt", "r") as f:
		count = 0
		for line in f:
			cols = line.split('\t')
			if len(cols)==9 and cols[8] == '1\n':
				st = ''
				for token in chunk_list[count].findall('token'):
					st = st + token.text+' '
				st = st.strip('\n')
				if(chunk_stat == 1):
					ET.SubElement(new_section, "chunk").text = st_chunk
					chunk_stat = 0
					st_chunk = ''
				new_section = ET.SubElement(xroot, "section")
				ET.SubElement(new_section, "heading").text = st
			elif(count<chunk_list_length) :
				chunk_stat =1
				for token in chunk_list[count].findall('token'):
					st_chunk = st_chunk + token.text+' '
				st_chunk = st_chunk.strip('\n')
			count = count + 1
	if chunk_stat == 1:
		 ET.SubElement(new_section, "chunk").text = st_chunk
	return xroot




"""
Token features as decimals
Special Sections    - 6
Single word chunk   - 5
Tables/Figures      - 0
Section Number      - 1
UpperCase token     - 2
Special Symbols     - 3
Rest                - 4
"""

def token_features(token_):
	token=token_.strip()
	parts=token.split('.')
	if(token=="Abstract" or token== "ABSTRACT" or token=="Acknowledgement" or token== "ACKNOWLEDGEMENT" or token=="References" or token== "Reference" or token == "REFERENCE" or token=="REFERENCES" or token=="Acknowledgements" or token== "ACKNOWLEDGEMENTS"):
		return "6"
	if(token=="$$$"):
		return "5"
	if token=="Table" or token=="TABLE" or token=="Figure" or token=="FIGURE" or token=="Fig.":
		return "0"
	p_len = len(parts)
	# For numerical tokens without decimal part
	if(p_len==1):
		if(token.isdigit() and 1<=int(token)<=20):
			return "1"
	# For tokens with decimal part		
	if(p_len==2 or p_len==3):
		if(parts[0].isdigit() and 1<=int(parts[0])<=20):
			if(parts[1]=='' or (parts[1].isdigit() and int(parts[1])<=20)):
				if(p_len==2):
					return "1"
				if(parts[1].isdigit() and int(parts[1])<=20 and parts[2]==''):
					return "1"
	# For tokens with Roman numerals				
	if(p_len==1 or (p_len==2 and parts[1]=='')):
		try:
			val = roman.fromRoman(parts[0].upper())
			if(val<=20):
				return "1"
		except:
			pass
		if((len(parts[0])==1 and 'A'<=parts[0]<='Z') or (len(parts[0])==3 and parts[0][0]=='(' and parts[0][2]==')' and parts[0][1].isalpha() and parts[0][1].isupper()) or (len(parts[0])==2 and parts[0][1]==')' and parts[0][0].isalpha() and parts[0][0].isupper())):
			if(p_len==1 or (p_len==2 and parts[1]=='')):
				return "1"
	# For tokens indexed using alphabets			
	if token[0].isupper():
		return "2" 
	if (not(parts[0].isalpha() or parts[0].isdigit())):
		return "3"
	return "4"


"""
Main function for section mapping
includes the pdftoxml file and the Path to the
file as parameters, path is defaulted to be the
current directory
"""


def sec_main(xroot,newxroot,modalFS):

	tree = ET.ElementTree(newxroot)
	
	newxroot = ET.Element("Document")
	ET.SubElement(newxroot, "chunk")

	previous_Font_Size = None
	# Refining the chunks in xroot using font sizes
	for chunks in xroot.findall('chunk'):
		chunk = ET.SubElement(newxroot, "chunk")
		count = 0
		stat = 0
		if(len(chunks)>20):
			stat = 1
		for token in chunks.findall('token'):
			if count < 15 and previous_Font_Size is not None and previous_Font_Size < float(token.attrib["font_size"]) and stat==1:
				chunk = ET.SubElement(newxroot, "chunk")
				ET.SubElement(chunk, "token", font_size=token.attrib['font_size'], bold=token.attrib['bold']).text = token.text
			else:
				ET.SubElement(chunk, "token", font_size=token.attrib['font_size'], bold=token.attrib['bold']).text = token.text
				count  = count + 1
			previous_Font_Size = float(token.attrib['font_size'])

	tree_NI = ET.ElementTree(newxroot)
	

	# Generating the final txt config file

	f = open(directory + 'input_out.txt','w')

	newxroot = tree.getroot()

	# Printing the token features into a file for tagging used CRF model on indexed inputs
	for _chunk in newxroot.findall('chunk'):
		boldness = 0
		Font_Size = 0
		tokens = _chunk.findall('token')
		if(len(tokens)==0):
			f.write('xxx\t0\t0\t0.0\t0\t0\t0\t0\n')
			continue
		elif(len(tokens) ==1):
			tok1 = '$$$'
			tok2 = tokens[0].text
		else:
			tok1 = tokens[0].text
			tok2 = tokens[1].text
		no_of_tokens = len(tokens)
		for t in tokens:
			if(t.attrib['bold']=="yes"):
				boldness=boldness+1
			Font_Size = Font_Size + float(t.attrib['font_size'])
		boldness = round(boldness/no_of_tokens,2)
		Font_Size = (Font_Size/no_of_tokens)/modalFS
		no_of_tokens = math.floor(no_of_tokens / 16)
		f.write(tok1+"\t"+tok2+"\t"+str(int(no_of_tokens))+"\t"+str(boldness)+"\t"+str(round(Font_Size,2))+"\t"+token_features(tok1)+"\t"+token_features(tok2)+"\t0\n")

	f.close()
	# Tagging used CRF model
	subprocess.call("crf_test -m mod2 " + 'input_out.txt'+" > " + "finalsec.txt", shell=True)

	f = open(directory + 'input_out_NI.txt','w')
	newxroot = tree_NI.getroot()

	# Printing the token features into a file for tagging used CRF model on non-indexed inputs
	for _chunk in newxroot.findall('chunk'):
		boldness = 0
		Font_Size = 0
		tokens = _chunk.findall('token')
		if(len(tokens)==0):
			f.write('xxx\t0\t0\t0.0\t0\t0\t0\t0\n')
			continue
		elif(len(tokens) ==1):
			tok1 = '$$$'
			tok2 = tokens[0].text
		else:
			tok1 = tokens[0].text
			tok2 = tokens[1].text
		no_of_tokens = len(tokens)
		for t in tokens:
			if(t.attrib['bold']=="yes"):
				boldness=boldness+1
			Font_Size = Font_Size + float(t.attrib['font_size'])
		boldness = round(boldness/no_of_tokens,2)
		Font_Size = (Font_Size/no_of_tokens)/modalFS
		no_of_tokens = math.floor(no_of_tokens / 16)
		f.write(tok1+"\t"+tok2+"\t"+str(int(no_of_tokens))+"\t"+str(boldness)+"\t"+str(round(Font_Size,2))+"\t"+token_features(tok1)+"\t"+token_features(tok2)+"\t0\n")

	f.close()

	# Tagging uing CRF model
	subprocess.call("crf_test -m model_4_1_16 " + directory + 'input_out.txt'+" > " + directory + "finalsec_NI.txt", shell=True)

	# Reading the tagged results
	secTree_I = generateXML(tree)
	secTree_NI = generateXML_NI(tree)

	journal_related = ["ACM", "Elsevier", "ELSEVIER", "arxiv", "ARXIV", "IEEE", "ieee", "CONFERENCE", "INTERNATIONAL",
					   "R E S E A R C H", "RESEARCH","DETECTION","Open"]


	xroot = ET.Element("sec_map")
	new_stat = 0
	new_head = 0
	# Refining the tags based journal based heuristic in indexed inputs
	for section in secTree_I.findall('section'):
		new_stat = 0
		new_head = 0
		new_section = ET.SubElement(xroot, "section")
		for _heading in section.findall('heading'):
			new_head = 1
			if(len(_heading.text.split())<=10):
				for x in journal_related:
					if(x in _heading.text):
						for chunk in section.findall("chunk"):
							ET.SubElement(new_section,"chunk").text =(_heading.text + " "+chunk.text)
						new_stat = 1
						break
				if(new_stat == 0):
					ET.SubElement(new_section,"heading").text = _heading.text
					for chunk in section.findall('chunk'):
						ET.SubElement(new_section,'chunk').text = chunk.text
			else:
				for chunk in section.findall("chunk"):
					ET.SubElement(new_section,"chunk").text =(_heading.text + " "+chunk.text)
		if(new_head == 0):
			for chunk in section.findall('chunk'):
				ET.SubElement(new_section,'chunk').text = chunk.text

	tree_I =  ET.ElementTree(xroot)



	xroot_NI = ET.Element("sec_map")
	new_stat = 0
	new_head = 0

	# Refining the tags based journal based heuristic in indexed inputs
	for section in secTree_NI.findall('section'):
		new_stat = 0
		new_head = 0
		new_section = ET.SubElement(xroot_NI, "section")
		for _heading in section.findall('heading'):
			new_head = 1
			if(len(_heading.text.split())<=10):
				for x in journal_related:
					if(x in _heading.text):
						for chunk in section.findall("chunk"):
							ET.SubElement(new_section,"chunk").text =(_heading.text + " "+chunk.text)
						new_stat = 1
						break
				if(new_stat == 0):
					ET.SubElement(new_section,"heading").text = _heading.text
					for chunk in section.findall('chunk'):
						ET.SubElement(new_section,'chunk').text = chunk.text
			else:
				for chunk in section.findall("chunk"):
					ET.SubElement(new_section,"chunk").text =(_heading.text + " "+chunk.text)
		if(new_head == 0):
			for chunk in section.findall('chunk'):
				ET.SubElement(new_section,'chunk').text = chunk.text

	tree_NI =  ET.ElementTree(xroot_NI)


	count_I =0
	count_NI =0

	# Deciding if an input is indexed or non-indexed
	for section in tree_I.findall("section"):
		for heading in section.findall("heading"):
			count_I = count_I+1
	for section in tree_NI.findall("section"):
		for heading in section.findall("heading"):
			count_NI = count_NI +1
	if count_I >= count_NI:
		root = tree_I.getroot()
		for section in root.findall("section"):
			candidate = section.find("chunk")
			if candidate is not None:
				if candidate.text is None or len(candidate.text.strip()) == 0:
					section.remove(candidate)
			elif section.find("heading") is None:
				root.remove(section)
		ET.ElementTree(root).write(directory + "Secmap.xml")
		

	if count_I < count_NI:
		root = tree_NI.getroot()
		for section in root.findall("section"):
			candidate = section.find("chunk")
			if candidate is not None:
				if candidate.text is None or len(candidate.text.strip()) == 0:
					section.remove(candidate)
			elif section.find("heading") is None:
				root.remove(section)
		ET.ElementTree(root).write(directory + "Secmap.xml")
		

