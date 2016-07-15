import xml.etree.ElementTree as ET
directory= '/var/www/html/OCR++/myproject/media/documents/'
out = open(directory + 'eval_cit2ref.txt','w')
tree = ET.parse(directory + 'input_res.xml')
root = tree.getroot()
cit2refs = root.find('Cit2ref')
for cit2ref in cit2refs.findall('cit2ref'):
	out.write('<<cit2ref>>\nCitation : '+cit2ref.text.strip()+"\nReference  : \n"+cit2ref.attrib['reference']+"\n")
out.close()
out = open(directory + 'eval_ref.txt','w')
refs = root.find('References')
for ref in refs.findall('Reference'):
	out.write('<<reference>> '+ref.text+'\n')
out.close()