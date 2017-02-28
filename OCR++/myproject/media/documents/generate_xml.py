import cPickle as pickle
import sys

# Note : TitleAuthor.xml is not made using Element Tree. Hence there may be errors in that file. Therefore not using it directly.

import xml.etree.ElementTree as ET
import sys
import unicodedata
import re
import pickle
from xml.sax.saxutils import escape

directory = '/var/www/html/OCR++/myproject/media/documents/'
'''
def generateXML(title,authors_list,aff_xml,emails_list,map_xml,urls_xml,sec_map_xml,footnotes_xml,tab_fig_xml,cit_ref_xml):

	root =  ET.Element("Document")
	tree = ET.ElementTree(root)
	
	titleElem = ET.SubElement(root,"Title")
	titleElem.text = title

	AuthorsElem = ET.SubElement(root,"Authors")
	for author in authors_list:
		AnAuthor = ET.SubElement(AuthorsElem,"Author")
		author_divided = author.split(' ')
		if len(author_divided)==1:
			first_name = author_divided[0]
			middle_name = ""
			last_name = ""
		elif len(author_divided)==2:
			first_name = author_divided[0]
			middle_name = ""
			last_name = author_divided[1]
		else:
			first_name = author_divided[0]
			last_name = author_divided[-1]
			middle_name = ""
			for midpart in author_divided[1:-1]:
				middle_name += midpart
				middle_name += " "
			middle_name = middle_name.strip() 

		AFirstName = ET.SubElement(AnAuthor,"First_Name")
		AFirstName.text = first_name
		AMiddleName = ET.SubElement(AnAuthor,"Middle_Name")
		AMiddleName.text = middle_name
		ALastName = ET.SubElement(AnAuthor,"Last_Name")
		ALastName.text = last_name

	# AffsElem = ET.SubElement(root,"Affliations")
	# for aff in affiliations_list:
	# 	AnAff = ET.SubElement(AffsElem,"Affliation")
	# 	AnAff.text = aff

	root.append(aff_xml)

	EmailsElem = ET.SubElement(root,"Emails")
	for email in emails_list:
		AnEmail = ET.SubElement(EmailsElem,"Email")
		AnEmail.text = email


	root.append(map_xml)
	root.append(sec_map_xml)
	root.append(tab_fig_xml)
	root.append(footnotes_xml)
	root.append(urls_xml)
	root.append(cit_ref_xml)

	tree = ET.ElementTree(root)
	tree.write(directory + 'output.xml')
'''
def getEveryThing():
	# title = open('temptitle.txt','r').read()
	# authors = open('file_for_names.txt','r').readlines()
	title_authors_xml = ET.parse(directory + 'TitleAuthor.xml').getroot()
	title = escape(title_authors_xml.find('title').text.strip())
	authors = []
	for author in title_authors_xml.findall('name'):
		try:
			first_name = author.find('first_name').text.strip()
		except:
			first_name = ""
		try:
			middle_name = author.find('middle_name').text.strip()
		except:
			middle_name = ""
		try:
			last_name = author.find('last_name').text.strip()
		except:
			last_name = ""
		if middle_name!="":
			authors.append(escape(first_name+" "+middle_name+" "+last_name))
		else:
			authors.append(escape(first_name+" "+last_name))
	# print authors
	emails = escape(open(directory + 'input_Allmails_for_map_temp.txt','r').read().replace('#e ','').strip()).split('\n')
	aff_xml = ET.parse(directory + 'input_AllAffiliations.txt').getroot()
	
	map_xml_wrong = ET.parse(directory + 'map.txt').getroot()
	map_xml_root = ET.Element('Author_Email_Map')
	map_xml = ET.ElementTree(map_xml_root).getroot()
	for map_ in map_xml_wrong:
		author = ""
		for name in (map_.text.split()[:-1]):
			author += name + " "
		email = map_.text.split()[-1]
		currentMap = ET.SubElement(map_xml_root,'Map')
		aut = ET.SubElement(currentMap,'Author')
		aut.text = escape(author)
		mail = ET.SubElement(currentMap,'Email')
		mail.text = escape(email)

	urls_xml = ET.parse(directory + 'URLop.txt').getroot()
	sec_map_xml = ET.parse(directory + 'Secmap.xml').getroot()
	footnotes_xml = ET.parse(directory + 'FOOTNOTEop.txt').getroot()
	tab_fig_xml = ET.parse(directory + 'TABFIGop.txt').getroot()
	cit_ref_xml = ET.parse(directory + 'input_res.xml').getroot()
	cit_ref_xml.tag = "Citations_And_References"
	return title,authors,aff_xml,emails,map_xml,urls_xml,sec_map_xml,footnotes_xml,tab_fig_xml,cit_ref_xml
'''
def main():
	title,authors,aff_xml,emails,map_xml,urls_xml,sec_map_xml,footnotes_xml,tab_fig_xml,cit_ref_xml = getEveryThing()
	generateXML(title,authors,aff_xml,emails,map_xml,urls_xml,sec_map_xml,footnotes_xml,tab_fig_xml,cit_ref_xml)
'''
# main()
def getPDFOrder():
	tree = ET.parse(directory+"input.xml")
	root = tree.getroot()
	s = ""
	for page in root.iter("PAGE"):
		for text in page.iter("TEXT"):
			for token in text.iter("TOKEN"):
				if token.text is None:
					continue
				if type(token.text) is unicode:
					s += unicodedata.normalize('NFKD', token.text).encode('ascii','ignore')
				else:
					s += token.text
				s +=" "
	s = escape(s.replace("- ",""))
	return s

# getPDFOrder()

def findPositions():
	pdf = getPDFOrder()
	title,authors,aff_xml,emails,map_xml,urls_xml,sec_map_xml,footnotes_xml,tab_fig_xml,cit_ref_xml = getEveryThing()
	
	titlePositions = (pdf.find(title),title,"<Title>")
	EveryThing = [titlePositions]
	# print title, titlePos
	authorPositions = []
	for author in authors:
		authorPositions.append((pdf.find(author),author,"<Author>"))
	# print authors, authorPositions
	EveryThing = EveryThing + authorPositions
	
	affiliationPositions = []
	for aff in aff_xml:
		aff.text = aff.text.strip()
		affiliationPositions.append((pdf.replace(",","").find(aff.text),aff.text,"<Affiliation>"))
	# print affiliationPositions
	EveryThing = EveryThing + affiliationPositions
	
	emailPositions = []
	for email in emails:
		email = email.strip()
		emailPositions.append((pdf.find(email),email,"<Email>"))
	# print emailPositions
	EveryThing = EveryThing + emailPositions
	
	urlPositions = []
	for URL in urls_xml:
		for url in URL:
			# print url.tag
			url.text = url.text.strip()
			urlPositions.append((pdf.find(url.text),url.text,"<URL>"))
	# print urlPositions
	EveryThing = EveryThing + urlPositions
	
	secHeadings = []
	secChunks = []
	for sec in sec_map_xml:
		for heading in sec.findall('heading'):
			heading.text = heading.text.strip()
			secHeadings.append((pdf.find(heading.text),escape(heading.text),"<SectionHeading>"))
		for chunk in sec.findall('chunk'):

			findFor = ("".join([x.strip()+" " for x in chunk.text.split(' ')[:5]])).strip()
			secChunks.append((pdf.find(findFor),escape(chunk.text.strip()),"<SectionChunk>"))
	# print secHeadings
	EveryThing = EveryThing + secHeadings
	EveryThing = EveryThing + secChunks
	# print secChunks
	
	footnotePositions = []
	for footnote in footnotes_xml:
		footnote.text = footnote.text.strip()
		footnotePositions.append((pdf.find(footnote.text),footnote.text,"<Footnote>"))
	# print footnotePositions
	EveryThing = EveryThing + footnotePositions
	
	tables = tab_fig_xml.find("Tables")
	figures = tab_fig_xml.find("Figures")
	tablePositions = []
	figurePositions = []
	for table in tables:
		table.text = table.text.strip()
		tablePositions.append((pdf.find(table.text),table.text,"<Table>"))
	for figure in figures:
		figure.text = figure.text.strip()
		figurePositions.append((pdf.find(figure.text),figure.text,"<Figure>"))
	# print tablePositions
	# print figurePositions
	EveryThing = EveryThing + tablePositions + figurePositions

	references = cit_ref_xml.find("References")
	citations = cit_ref_xml.find("Cit2ref")
	referencePositions = []
	citationPositions = []
	minRef = 1000000000
	for ref in references:
		ref.text = ref.text.strip()
		pos = pdf.find(ref.text.replace('- ',''))
		minRef = min(pos,minRef)
		referencePositions.append((pos,ref.text.replace('- ',''),"<Reference>"))
	# print referencePositions
	EveryThing = EveryThing + referencePositions

	pdfWithoutReferences = pdf[:minRef]
	for cit in citations:
		# re.escape changes cit.text so that it does not mean anything else as a regex (Adds '\' wherever neccessary)
		thisReferenceCitedAt = [m.start() for m in re.finditer(re.escape(cit.text),pdfWithoutReferences)]
		# print thisReferenceCitedAt, pdfWithoutReferences.find(cit.text)

	return sorted(EveryThing),pdf

def main():
	
	EveryThing,pdf = findPositions()
	outputs = EveryThing

	final = []
	headingFound = False
	stack = []
	indexStack = []
	emptyStack = True

	temp = []
	for op in outputs:
		if op[0]==-1:
			continue;
		if(op[2] == '<SectionChunk>'):
			if(headingFound):
				headingFound = False
			else:
				continue
		if(op[2] == '<SectionHeading>'):
			headingFound = True

		temp.append(op);

	outputs = temp


	for op in range(len(outputs)):

		elem = []
		elem.append(outputs[op][2])
		elem.append(outputs[op][0])
		elem.append(outputs[op][0] + len(outputs[op][1]))
		

		if op < (len(outputs)-1):
			if elem[2] <= outputs[op+1][0]:
				if len(indexStack)>0:
					while(indexStack[-1] <= outputs[op+1][0]):
						# print stack[-1]
						final.append("</" + stack[-1][1:])
						stack = stack[:-1]
						indexStack = indexStack[:-1]
						if len(indexStack) == 0 or len(stack) == 0:
							break

				final.append(elem)
				stack.append(outputs[op][2])
				final.append("</" + stack[-1][1:])
				stack = stack[:-1]

			else:
				final.append(elem)
				stack.append(outputs[op][2])

				if op == (len(outputs)-1):
					final.append("</" + stack[-1][1:])
					stack = stack[:-1]
				
				
				
				else:
					# print elem[2]
					indexStack.append(elem[2])


		else:

			final.append(elem)
			stack.append(outputs[op][2])

			if op == (len(outputs)-1):
				final.append("</" + stack[-1][1:])
				stack = stack[:-1]
					
			else:
				indexStack.append(elem[2])

	while len(stack)>0:
		final.append("</" + stack[-1][1:])
		stack = stack[:-1]

	# def tabs(stack):
	# 	for i in range(len(stack)):
	# 		sys.stdout.write("\t")

	tabStack = []
	stack = []
	pointer = 0

	# for f in final:
	# 	print f

	stringOutput = ''

	stringOutput +=  '<Document>'

	for f in final:
		if len(f) == 3:
			# tabStackbs(stack)
			stack.append(f[2])
			if pointer < f[1]:
				for i in range(pointer,f[1]-1,1):
					stringOutput += (pdf[i])

			pointer = f[1]

			stringOutput +=  f[0] + ' '

		else:
			if pointer < stack[-1]:
				for i in range(pointer,min(stack[-1],len(pdf)),1):
					stringOutput += (pdf[i])

			pointer = stack[-1]
			stack = stack[:-1]

			stringOutput +=  f + ' '

	stringOutput +=  "</Document>"

	with open(directory + 'output.xml','w') as output:
		output.write(stringOutput)

	return stringOutput



# s = main()
# print s