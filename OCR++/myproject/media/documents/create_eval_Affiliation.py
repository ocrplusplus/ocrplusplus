import xml.etree.ElementTree as ET
directory= '/var/www/html/OCR++/myproject/media/documents/'
out = open(directory + 'eval_Affiliations.txt','w')
tree = ET.parse(directory + "input_AllAffiliations.txt")
root = tree.getroot()
for affs in root.findall('Affiliation'):
    out.write("<<Affiliation>> " + affs.text.strip().replace("%27","&") + "\n")
out.close()

