author = "barno"

directory = '/var/www/html/OCR++/myproject/media/documents/'


flag = "0"   # to check if a title is already going on
end = 0
titl = 0;
# print("<?xml version=\"1.0\" ?>\n")
# print("<title_author>\n")
fi = open(directory + 'test_aut.txt','w')
titl_done = 0
tokens = 0
caps = 0
upper = 0
possible_titles = []
# titl_ext = "<?xml version=\"1.0\" ?>\n<title_author>\n"
titl_ext = ""
relpos = 0
relsize = 0
pos = []
size = []
maxsize = 0
secmaxsize = 0
lineno = 0
temp = ""
titllen = 0
lines = []
ex_y = 0
sizes = []
maxsz = 0
with open(directory + 'final.txt','r') as f:
	for line in f:
		abc = line.split()

		if len(abc) > 1:  # if not a blank line

			

			if float(abc[4]) > maxsize:
				secmaxsize = maxsize
				maxsize = float(abc[4])

			if float(abc[4]) > secmaxsize and float(abc[4]) < maxsize :
				secmaxsize = float(abc[4])
			# print "***" + abc[0]
			abc[0] = abc[0].replace('&','&amp;')

			# if(abc[9]=="00"):
			# 	print

			if abc[0]=="00":
				# titl_done = 1
				continue
			temp = abc[0]
			lines.append(line)
			if titl_done == 0:
			    if abc[12] == "1":   #output column
			    	titl = 1;
			    	titllen = titllen + len(abc[0])
			    	# if flag == "0":  #if start of title
			    	# 	titl_ext = titl_ext + "\t<title>\n\t"
			    	if abc[3] != relpos or abc[4] != relsize:
			    		possible_titles.append(titl_ext)
			    		titl_ext = ""
			    		relpos = abc[3]
			    		relsize = abc[4]
			    		pos.append(abc[3])
			    		size.append(abc[4])
		    		if float(abc[4])>maxsz:
		    			maxsz = float(abc[4])
		    		sizes.append(abc[4])
			    		# print "here1"
			    	titl_ext = titl_ext + abc[0] + " "
			    	flag = "1"
			    	fi.write(line)
			    else:
			    	if abc[0] != "0" and flag == "1":
			    		if(titl==1):
			    			# print("\n\t</title>")
			    			# if titllen > 10:
		    				titl_done = 1
			    			possible_titles.append(titl_ext)
			    			titl_ext = ""
				    		pos.append(relpos)
				    		size.append(relsize)
			    			titl = 0;
			    			if lineno==1 and abc[0]==temp:
			    				k = 1
			    			else:  
			    				# print "yo"
			    				if ex_y!=float(abc[8]):
	    							fi.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
			    				if ',' in abc[0]:
			    					for a in abc[:-1]:
			    						fi.write(a.replace(',','')+"\t")
			    					fi.write(abc[-1]+"\n,\t")
			    					for a in abc[1:-1]:
			    						fi.write(a.replace(',','')+"\t")
			    					fi.write(abc[-1]+"\n")
			    				else:
			    					fi.write(line)
			    			lineno = lineno + 1
			    			# print "here2"
			    		flag = "0"
			    		
			    		# print

			    if abc[12] == "2": #first name
			    	if(titl==1):
			    			# print("\n\t</title>")
			    			# if titllen > 10:
		    				titl_done = 1	
			    			possible_titles.append(titl_ext)
			    			titl_ext = ""
				    		pos.append(relpos)
				    		size.append(relsize)
			    			titl = 0;
			    			# print "here3"
			    	x = abc[0].strip(',')
			    	# print lineno
			    	# print abc[0]
			    	# print temp
	    			if lineno==1 and abc[0]==temp:
	    				k = 1
	    			else:  
	    				if ex_y!=float(abc[8]):
	    					fi.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
	    				if ',' in abc[0]:
	    					for a in abc[:-1]:
	    						fi.write(a.replace(',','')+"\t")
	    					fi.write(abc[-1]+"\n,\t")
	    					for a in abc[1:-1]:
	    						fi.write(a.replace(',','')+"\t")
	    					fi.write(abc[-1]+"\n")
	    				else:
	    					fi.write(line)
	    			lineno = lineno + 1
			else:
				if abc[12] == '1':
					relpos = abc[3]
					relsize = abc[4]
					if float(abc[4])>maxsz:
						maxsz = float(abc[4])
					sizes.append(abc[4])
					titl_ext = titl_ext + abc[0] + " "
					
				# if abc[5] == '0': 
				# 	if caps == 1:
				# 		fi.write("00\t00\t00\t00\t00\t00\t00\t00\t00\t00\t00\t00\t00\n")
				# 	caps = 0
				# if abc[5] == '1': 
				# 	if caps == 0:
				# 		fi.write("00\t00\t00\t00\t00\t00\t00\t00\t00\t00\t00\t00\t00\n")
				# 	caps = 1

				if ',' in abc[0]:
					if len(abc[0]) > 1:
					    line = line.strip(abc[0])
					    abc[0] = abc[0].strip(',')
					    line = abc[0] + line + ',' + line

			   	if ex_y!=float(abc[8]):
					fi.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
				if ',' in abc[0]:
					for a in abc[:-1]:
						fi.write(a.replace(',','')+"\t")
					fi.write(abc[-1]+"\n,\t")
					for a in abc[1:-1]:
						fi.write(a.replace(',','')+"\t")
					fi.write(abc[-1]+"\n")
				else:
					fi.write(line)
			   	if abc[0] != '00':
			   		tokens = tokens + 1
			   	if tokens >= 120:
			   		break
			ex_y = float(abc[8])

fi.close()	


if len(titl_ext) < 6:
	with open(directory + 'test_aut.txt','w') as fia:
		no = 0
		for line in lines:
			abc=line.split()
			if ex_y!=float(abc[8]):
				fia.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
			if ',' in abc[0]:
				for a in abc[:-1]:
					fia.write(a.replace(',','')+"\t")
				fia.write(abc[-1]+"\n,\t")
				for a in abc[1:-1]:
					fia.write(a+"\t")
				fia.write(abc[-1]+"\n")
			else:
				fia.write(line)
			# fia.write("\n")
			no = no + 1
			if no == 120:
				# fia.close()
				break
			ex_y = float(abc[8])
			# fia.close()

# print sizes
# print maxsz
# print titl_ext.split()
# print possible_titles
tlt = ""
for tt in possible_titles:
	ttt = tt.split()
	for tt in ttt:
		tlt = tlt + tt + " "
tlt = tlt + titl_ext

# print len(sizes)
# print maxsz
# print len(tlt.split())
# print sizes
# print maxsz
# print tlt.split()
if len(sizes) == len(tlt.split()) and len(sizes)>0:
	# print "yo"
	tempt = tlt.split()
	titl_ext = ""
	for i in range(0,len(sizes)):
		if float(sizes[i])==maxsz:
			titl_ext = titl_ext + tempt[i] + " "

# print titl_ext
possible_titles = []
possible_titles.append(titl_ext)
pos.append(relpos)
size.append(relsize)
titl_ext = ""
# print possible_titles
# print pos
# print size


it = []
for i in range(0,len(possible_titles)):
	# print i
	# print possible_titles[i].split()
	if len(possible_titles[i].split())>0 and len(possible_titles[i].split())<=25:
		it.append(i)
		# print i

# print it

# if len(it)==0:
# 	possible_titles.append('S')
# 	pos.append('0.5')
# 	size.append('0.5')
# 	it.append(1)

lpos = it[0]
msize = it[0]
for i in it:
	if float(pos[lpos]) > float(pos[i]):
		lpos = i
	if float(size[msize]) < float(size[i]):
		msize = i
# print msize
# print lpos
fi=[]

for i in it:
	if float(pos[lpos]) == float(pos[i]):
		if i not in fi:
			fi.append(i)
	if float(size[msize]) == float(size[i]):
		if i not in fi:
			fi.append(i)

arx = 0

if msize == lpos:
	# titl_ext = possible_titles[msize]
	for i in fi:
		tx = possible_titles[i]
		if "arXiv:" in tx:
			tx = ""
			arx = 1
		# print tx
		titl_ext = titl_ext + tx
else:
	for i in range(0,len(it)):
		# if len(titl_ext.split())<=225:
		titl_ext = titl_ext + possible_titles[i] + " "

for l in lines:
	if "arXiv:" in l:
		tx = ""
		arx = 1

# print titl_ext

# print maxsize
# print secmaxsize

if arx == 1 or len(titl_ext.split())<2:
	titl_ext = ""
	with open(directory + 'final.txt','r') as f:
		for line in f:
			abc = line.split()

			if len(abc) > 1:
				# print secmaxsize
				if float(abc[4]) == secmaxsize:
					# if len(titl_ext) <= 225:
					#print abc[0]
					titl_ext = titl_ext + abc[0] + " "


affils = []
with open(directory + 'input_AllAffiliations.txt','r') as f:
	for line in f:
		if "Affiliation" in line:
			continue
		line = line.strip('\t')
		line = line.strip('\n')
		affils.append(line)

# print titl_ext
for a in affils:
	if a in titl_ext:
		titl_ext = titl_ext.replace(a,'')


# if len(titl_ext)<2:
# 	print maxsize
# 	 with open(directory + 'final.txt','r') as f:
# 		for line in f:
# 			abc = line.split()

# 			if len(abc) > 1:
# 				if float(abc[4]) == maxsize:
# 					titl_ext = titl_ext + abc[0] + " "

# print "yo" + titl_ext

if "Conference" in titl_ext or "IEEE" in titl_ext or "ACM" in titl_ext or "JOURNAL" in titl_ext or "Journal" in titl_ext:
	titl_ext = ""


# print possible_titles
# print fi
# print titl_ext

if len(titl_ext)<5 or titl_ext == "Case study ":
	# print maxsize
	# print "yo"	
	with open(directory + 'final.txt','r') as f:
		for line in f:
			abc = line.split()

			if len(abc) > 1:
				if float(abc[4]) == maxsize:
					titl_ext = titl_ext + abc[0] + " "

wrds = titl_ext.split()
if len(wrds) >25:
	titl_ext = ""
	for i in range(0,25):
		titl_ext = titl_ext + wrds[i] + " "

# print possible_titles

wrds = titl_ext.split()
if ''.join([i for i in wrds[0] if not i.isdigit()]).isupper() and ''.join([i for i in wrds[1] if not i.isdigit()]).isupper() and ''.join([i for i in wrds[2] if not i.isdigit()]).isupper():
	titl_ext = ""
	for w in wrds:
		if not ''.join([i for i in w if not i.isdigit()]).isupper():
			break
		titl_ext = titl_ext + w + " "

temp = open(directory + 'temptitle.txt','w')
temp.write(titl_ext)
temp.close()

titl_ext = "<?xml version=\"1.0\" ?>\n<title_author>\n\t<title>\n\t" + titl_ext
print titl_ext
print "\n\t</title>"        	
# print("</title_author>\n")




