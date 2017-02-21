
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
Create an XML of headings and sections
"""
def generateXML(tree):
	rt = tree.getroot()
	ls = rt.findall('chunk')
	st_chunk = ''
	sp_length = len(ls)
	chunk_stat =0
	xroot = ET.Element("sec_map")
	new_section = ET.SubElement(xroot, "section")
	with open(directory + "finalsec.txt", "r") as f:
		count = 0
		for line in f:
			cols = line.split('\t')
			if len(cols)==9 and cols[8] == '1\n':
				st = ''
				for token in ls[count].findall('token'):
					st = st + token.text+' '
				st = st.strip('\n')
				if(chunk_stat == 1):
					ET.SubElement(new_section, "chunk").text = st_chunk
					chunk_stat = 0
					st_chunk = ''
				new_section = ET.SubElement(xroot, "section")
				ET.SubElement(new_section, "heading").text = st
			elif(count<sp_length) :
				chunk_stat =1
				for token in ls[count].findall('token'):
					st_chunk = st_chunk + token.text+' '
				st_chunk = st_chunk.strip('\n')
			count = count + 1
	if chunk_stat == 1:
		 ET.SubElement(new_section, "chunk").text = st_chunk
	return xroot


def generateXML_NI(tree):
	rt = tree.getroot()
	ls = rt.findall('chunk')
	st_chunk = ''
	sp_length = len(ls)
	chunk_stat =0
	xroot = ET.Element("sec_map")
	new_section = ET.SubElement(xroot, "section")
	with open(directory + "finalsec_NI.txt", "r") as f:
		count = 0
		for line in f:
			cols = line.split('\t')
			if len(cols)==9 and cols[8] == '1\n':
				st = ''
				for token in ls[count].findall('token'):
					st = st + token.text+' '
				st = st.strip('\n')
				if(chunk_stat == 1):
					ET.SubElement(new_section, "chunk").text = st_chunk
					chunk_stat = 0
					st_chunk = ''
				new_section = ET.SubElement(xroot, "section")
				ET.SubElement(new_section, "heading").text = st
			elif(count<sp_length) :
				chunk_stat =1
				for token in ls[count].findall('token'):
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

def token_features(y):
	x=y.strip()
	parts=x.split('.')
	if(x=="Abstract" or x== "ABSTRACT" or x=="Acknowledgement" or x== "ACKNOWLEDGEMENT" or x=="References" or x== "Reference" or x == "REFERENCE" or x=="REFERENCES" or x=="Acknowledgements" or x== "ACKNOWLEDGEMENTs"):
		return "6"
	if(x=="$$$"):
		return "5"
	if x=="Table" or x=="TABLE" or x=="Figure" or x=="FIGURE" or x=="Fig.":
		return "0"
	p_len = len(parts)
	if(p_len==1):
		if(x.isdigit() and 1<=int(x)<=20):
			return "1"
	if(p_len==2 or p_len==3):
		if(parts[0].isdigit() and 1<=int(parts[0])<=20):
			if(parts[1]=='' or (parts[1].isdigit() and int(parts[1])<=20)):
				if(p_len==2):
					return "1"
				if(parts[1].isdigit() and int(parts[1])<=20 and parts[2]==''):
					return "1"
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
	if x[0].isupper():
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

# def secmap(ff, path=""):
def sec_main(xroot,newxroot,modalFS):

	tree = ET.ElementTree(newxroot)
	
	newxroot = ET.Element("Document")
	ET.SubElement(newxroot, "chunk")

	preFS = None
	for chunks in xroot.findall('chunk'):
		chunk = ET.SubElement(newxroot, "chunk")
		count = 0
		stat = 0
		if(len(chunks)>20):
			stat = 1
		for token in chunks.findall('token'):
			if count < 15 and preFS is not None and preFS < float(token.attrib["font_size"]) and stat==1:
				chunk = ET.SubElement(newxroot, "chunk")
				ET.SubElement(chunk, "token", font_size=token.attrib['font_size'], bold=token.attrib['bold']).text = token.text
			else:
				ET.SubElement(chunk, "token", font_size=token.attrib['font_size'], bold=token.attrib['bold']).text = token.text
				count  = count + 1
			preFS = float(token.attrib['font_size'])

	tree_NI = ET.ElementTree(newxroot)
	# tree_NI.write(ff+"_fin_NI.xml")

	# Generating the final txt config file

	f = open(directory + 'input_out.txt','w')

	newxroot = tree.getroot()

	for achunk in newxroot.findall('chunk'):
		boldness = 0
		fsize = 0
		tokens = achunk.findall('token')
		if(len(tokens)==0):
			f.write('xxx\t0\t0\t0.0\t0\t0\t0\t0\n')
			continue
		elif(len(tokens) ==1):
			tok1 = '$$$'
			tok2 = tokens[0].text
		else:
			tok1 = tokens[0].text
			tok2 = tokens[1].text
		tcount = len(tokens)
		for t in tokens:
			if(t.attrib['bold']=="yes"):
				boldness=boldness+1
			fsize = fsize + float(t.attrib['font_size'])
		boldness = round(boldness/tcount,2)
		fsize = (fsize/tcount)/modalFS
		tcount = math.floor(tcount / 16)
		f.write(tok1+"\t"+tok2+"\t"+str(int(tcount))+"\t"+str(boldness)+"\t"+str(round(fsize,2))+"\t"+token_features(tok1)+"\t"+token_features(tok2)+"\t0\n")

	f.close()
	subprocess.call("crf_test -m mod2 " + 'input_out.txt'+" > " + "finalsec.txt", shell=True)

	f = open(directory + 'input_out_NI.txt','w')
	newxroot = tree_NI.getroot()

	for achunk in newxroot.findall('chunk'):
		boldness = 0
		fsize = 0
		tokens = achunk.findall('token')
		if(len(tokens)==0):
			f.write('xxx\t0\t0\t0.0\t0\t0\t0\t0\n')
			continue
		elif(len(tokens) ==1):
			tok1 = '$$$'
			tok2 = tokens[0].text
		else:
			tok1 = tokens[0].text
			tok2 = tokens[1].text
		tcount = len(tokens)
		for t in tokens:
			if(t.attrib['bold']=="yes"):
				boldness=boldness+1
			fsize = fsize + float(t.attrib['font_size'])
		boldness = round(boldness/tcount,2)
		fsize = (fsize/tcount)/modalFS
		tcount = math.floor(tcount / 16)
		f.write(tok1+"\t"+tok2+"\t"+str(int(tcount))+"\t"+str(boldness)+"\t"+str(round(fsize,2))+"\t"+token_features(tok1)+"\t"+token_features(tok2)+"\t0\n")

	f.close()


	# subprocess.call("crf_test -m mod_10_1 " + ff.split('.')[0]+'_out.txt'+" > " + directory + "finalsec_NI.txt", shell=True)
	subprocess.call("crf_test -m model_4_1_16 " + directory + 'input_out.txt'+" > " + directory + "finalsec_NI.txt", shell=True)


	secTree_I = generateXML(tree)
	secTree_NI = generateXML_NI(tree)

	journal_related = ["ACM", "Elsevier", "ELSEVIER", "arxiv", "ARXIV", "IEEE", "ieee", "CONFERENCE", "INTERNATIONAL",
					   "R E S E A R C H", "RESEARCH","DETECTION","Open"]


	xroot = ET.Element("sec_map")
	new_stat = 0
	new_head = 0

	for section in secTree_I.findall('section'):
		new_stat = 0
		new_head = 0
		new_section = ET.SubElement(xroot, "section")
		for aheading in section.findall('heading'):
			# print(aheading.text)
			new_head = 1
			if(len(aheading.text.split())<=10):
				for x in journal_related:
					if(x in aheading.text):
						for chunk in section.findall("chunk"):
							ET.SubElement(new_section,"chunk").text =(aheading.text + " "+chunk.text)
						new_stat = 1
						break
				if(new_stat == 0):
					ET.SubElement(new_section,"heading").text = aheading.text
					for chunk in section.findall('chunk'):
						ET.SubElement(new_section,'chunk').text = chunk.text
			else:
				for chunk in section.findall("chunk"):
					ET.SubElement(new_section,"chunk").text =(aheading.text + " "+chunk.text)
		if(new_head == 0):
			for chunk in section.findall('chunk'):
				ET.SubElement(new_section,'chunk').text = chunk.text

	tree_I =  ET.ElementTree(xroot)

	# cc =  ET.tostring(xroot, 'utf-8')
	# reparsed = xml.dom.minidom.parseString(cc)
	# print reparsed.toprettyxml(indent="\t")


	xroot_NI = ET.Element("sec_map")
	new_stat = 0
	new_head = 0

	for section in secTree_NI.findall('section'):
		new_stat = 0
		new_head = 0
		new_section = ET.SubElement(xroot_NI, "section")
		for aheading in section.findall('heading'):
			new_head = 1
			if(len(aheading.text.split())<=10):
				for x in journal_related:
					if(x in aheading.text):
						for chunk in section.findall("chunk"):
							ET.SubElement(new_section,"chunk").text =(aheading.text + " "+chunk.text)
						new_stat = 1
						break
				if(new_stat == 0):
					ET.SubElement(new_section,"heading").text = aheading.text
					for chunk in section.findall('chunk'):
						ET.SubElement(new_section,'chunk').text = chunk.text
			else:
				for chunk in section.findall("chunk"):
					ET.SubElement(new_section,"chunk").text =(aheading.text + " "+chunk.text)
		if(new_head == 0):
			for chunk in section.findall('chunk'):
				ET.SubElement(new_section,'chunk').text = chunk.text

	tree_NI =  ET.ElementTree(xroot_NI)


	count_I =0
	count_NI =0
	for section in tree_I.findall("section"):
		for heading in section.findall("heading"):
			count_I = count_I+1
	for section in tree_NI.findall("section"):
		for heading in section.findall("heading"):
			count_NI = count_NI +1
	if count_I >= count_NI:
		#print ("Indexed!")
		tree_I.write(directory + "Secmap.xml")
		# root = tree_I.getroot()
		# f = open('eval_secmap.txt','w')
		# for section in root.findall('section'):
		# 	heads = section.findall('heading')
		# 	chunks = section.findall('chunk')
		# 	# print "<<section>>"
		# 	f.write("<<section>>\n")
		# 	if(len(heads)>0):
		# 		# print "Heading: "+heads[0].text
		# 		f.write("Heading: "+heads[0].text+"\n")
		# 	if(len(chunks)>0):
		# 		cw = chunks[0].text.split()
		# 		# print "Chunks: "+" ".join(cw[:5])+" ... "+" ".join(cw[-5:])
		# 		f.write("Chunks: "+" ".join(cw[:5])+" ... "+" ".join(cw[-5:])+"\n")
		# f.close()


	if count_I < count_NI:
		#print ("Non-Indexed!")
		tree_NI.write(directory + "Secmap.xml")
		#root = tree_NI.getroot()
		# f = open('eval_secmap.txt','w')
		# for section in root.findall('section'):
		# 	heads = section.findall('heading')
		# 	chunks = section.findall('chunk')
		# 	# print "<<section>>"
		# 	f.write("<<section>>\n")
		# 	if(len(heads)>0):
		# 		# print "Heading: "+heads[0].text
		# 		f.write("Heading: "+heads[0].text+"\n")
		# 	if(len(chunks)>0):
		# 		cw = chunks[0].text.split()
		# 		# print "Chunks: "+" ".join(cw[:5])+" ... "+" ".join(cw[-5:])
		# 		f.write("Chunks: "+" ".join(cw[:5])+" ... "+" ".join(cw[-5:])+"\n")
		# f.close()

	# cc =  ET.tostring(xroot_NI, 'utf-8')
	# reparsed = xml.dom.minidom.parseString(cc)
	# print reparsed.toprettyxml(indent="\t")

