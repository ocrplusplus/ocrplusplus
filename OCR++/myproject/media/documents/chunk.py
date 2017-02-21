import operator
import xml.etree.ElementTree as ET
import unicodedata
def chunk_1(root):
	preYLOC = None
	yDiff={}
	fontSizes = {}
	directory = ''

	for pages in root.findall('PAGE'):
		preYLOC=0
		for texts in pages.findall('TEXT'):
			for token in texts.findall('TOKEN'):
				try:
					fontSizes[round(abs(float(token.attrib['font-size'])))]=fontSizes.get(round(abs(float(token.attrib['font-size']))),0)+1
					if(preYLOC is None):
						preYLOC=float(token.attrib['y'])
					yDiff[round(abs(float(token.attrib['y'])-preYLOC))]=yDiff.get(round(abs(float(token.attrib['y'])-preYLOC)),0)+1
					preYLOC=float(token.attrib['y'])
				except:
					pass

	modalFS = 0
	# Find Modal Font size
	for FS in fontSizes.keys():
		if(modalFS == 0):
			modalFS = FS
			continue
		if(fontSizes[FS]>fontSizes[modalFS]):
			modalFS=FS

	# Finding modal Y difference
	new_l = sorted(yDiff.iteritems(), key=operator.itemgetter(1), reverse=True)[:7]
	x_l = []
	# print(new_l)
	for k in new_l:
		if(k[0]>6.0):
			x_l.append(k)
	new_l=x_l

	x_l=[]
	mode=new_l[0][1]
	for k in new_l:
		if(not(k[1]<=mode/2 or abs(new_l[0][0]-k[0])>=4)):
			x_l.append(k)

	new_l=x_l
	# print(new_l)
	del x_l

	limit = max([x[0] for x in new_l])+1
	# print(limit)

	# Create new XML file for Chunks
	preYLOC = None
	page_count =0
	xroot = ET.Element("Document")
	chunk = ET.SubElement(xroot, "chunk")
	for pages in root.findall('PAGE'):
		page_count = page_count +1
		for texts in pages.findall('TEXT'):
			for token in texts.findall('TOKEN'):
				if type(token.text) is unicode:
					word = unicodedata.normalize('NFKD', token.text).encode('ascii','ignore')
				else:
					word = token.text
				if(word and len(word.replace(' ',''))>0):
					if(preYLOC is None):
						preYLOC = float(token.attrib['y'])
						ET.SubElement(chunk, "token", font_size=token.attrib['font-size'], bold=token.attrib['bold'],page_number = str(page_count),y = token.attrib['y']).text = word
						continue
					if(abs(float(token.attrib['y'])-preYLOC)>=limit):
						chunk = ET.SubElement(xroot, "chunk")
					preYLOC = float(token.attrib['y'])
					ET.SubElement(chunk, "token", font_size=token.attrib['font-size'], bold=token.attrib['bold'],page_number =str(page_count),y = token.attrib['y']).text = word

	#tree = ET.ElementTree(xroot)
	return xroot,modalFS

def chunk_2(root):
	newxroot = ET.Element("Document")
	ET.SubElement(newxroot, "chunk")

	preFS = None
	max_font_size = 0

	# Refining chunks to strip leading headings FOR INDEXED PDFS
	for chunks in root.findall('chunk'):
		chunk = ET.SubElement(newxroot, "chunk")
		count = 0
		stat = 0
		if(len(chunks)>20):
			stat = 1
		for token in chunks.findall('token'):
			if float(token.attrib["font_size"])>max_font_size:
				max_font_size = float(token.attrib["font_size"])

			if (count < 15) and (preFS is not None) and (float(token.attrib["font_size"]) < preFS) and (stat==1):
				chunk = ET.SubElement(newxroot, "chunk")
				ET.SubElement(chunk, "token", font_size=token.attrib['font_size'], bold=token.attrib['bold']).text = token.text
			else:
				ET.SubElement(chunk, "token", font_size=token.attrib['font_size'], bold=token.attrib['bold']).text = token.text
				count  = count + 1
			preFS = float(token.attrib['font_size'])
			

	return newxroot, max_font_size