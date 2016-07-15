# Note : TitleAuthor.xml is not made using Element Tree. Hence there may be errors in that file. Therefore not using it directly.

import xml.etree.ElementTree as ET
import sys

directory = '/var/www/html/OCR++/myproject/media/documents/'

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

def getEveryThing():
	# title = open('temptitle.txt','r').read()
	# authors = open('file_for_names.txt','r').readlines()
	title_authors_xml = ET.parse(directory + 'TitleAuthor.xml').getroot()
	title = title_authors_xml.find('title').text.strip()
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
		authors.append(first_name+" "+middle_name+" "+last_name)
	# print authors
	emails = open(directory + 'input_Allmails_for_map_temp.txt','r').read().replace('#e ','').strip().split('\n')
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
		aut.text = author
		mail = ET.SubElement(currentMap,'Email')
		mail.text = email

	urls_xml = ET.parse(directory + 'URLop.txt').getroot()
	sec_map_xml = ET.parse(directory + 'Secmap.xml').getroot()
	footnotes_xml = ET.parse(directory + 'FOOTNOTEop.txt').getroot()
	tab_fig_xml = ET.parse(directory + 'TABFIGop.txt').getroot()
	cit_ref_xml = ET.parse(directory + 'input_res.xml').getroot()
	cit_ref_xml.tag = "Citations_And_References"
	return title,authors,aff_xml,emails,map_xml,urls_xml,sec_map_xml,footnotes_xml,tab_fig_xml,cit_ref_xml

def main():
	title,authors,aff_xml,emails,map_xml,urls_xml,sec_map_xml,footnotes_xml,tab_fig_xml,cit_ref_xml = getEveryThing()
	generateXML(title,authors,aff_xml,emails,map_xml,urls_xml,sec_map_xml,footnotes_xml,tab_fig_xml,cit_ref_xml)

main()