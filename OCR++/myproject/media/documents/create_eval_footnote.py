import xml.etree.ElementTree as ET
directory = '/var/www/html/OCR++/myproject/media/documents/'

f = open(directory + "FOOTNOTEop.txt",'r')
out = open(directory + 'eval_footnote.txt','w')
xml = f.read()
tree = ET.ElementTree(ET.fromstring(xml))
root = tree.getroot()
for foot in root.findall('footnote'):
    out.write("<<footnote>>\n" + foot.text.strip() + "\n")
f.close()
out.close()