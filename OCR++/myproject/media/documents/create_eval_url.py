import xml.etree.ElementTree as ET
directory = '/var/www/html/OCR++/myproject/media/documents/'
f = open(directory + "URLop.txt",'r')
out = open(directory + 'eval_url.txt','w')
xml = f.read()
tree = ET.ElementTree(ET.fromstring(xml))
root = tree.getroot()
for URL in root.findall('URL'):
    for url in URL.findall('url'):
        out.write("<<url>>\n" + url.text.strip() + "\n")
f.close()
out.close()