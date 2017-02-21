import xml.etree.ElementTree as ET
directory = '/var/www/html/OCR++/myproject/media/documents/'
f = open(directory + "TABFIGop.txt",'r')
out = open(directory + 'eval_tables_figures.txt','w')
xml = f.read()
tree = ET.ElementTree(ET.fromstring(xml))
root = tree.getroot()
for tab in root.findall('Tables'):
    for table in tab.findall('table'):
        out.write("<<table>>\n" + table.text.strip() + "\n")

out.write("\n")

for fig in root.findall('Figures'):
    for figure in fig.findall('figure'):
        out.write("<<figure>>\n" + figure.text.strip() + "\n")

f.close()
out.close()