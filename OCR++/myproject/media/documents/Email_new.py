import xml.etree.ElementTree as ET
import unicodedata
import operator
import copy
import re

# Binary converter for strings
def binary(x):
    if x == "yes":
        return "1"
    return "0"

########################################PRIYANK#####################################################

def isEmail(y):
    x=y.strip()
    x = x.strip('.')
    isatr = 0
    for i in range(len(x)):
        if x[i] == "@":
            isatr = 1
        if((isatr==1) and (x[i]==".")):# and (x[i+1]<"z" and x[i+1]>"a")):
            return "1"
    return "0"


foutMail = "0\t0\t0\n"
# foutMail = open(directory + 'input_mail_parse.txt','w')
# foutMail.write("0\t0\t0\n")
directory= '/var/www/html/OCR++/myproject/media/documents/'#raw_input()+"/"#/home/priyank/Desktop/Projects/pdfs/"
	


def processTokenForMail(word,p,alp,bracks):
	global foutMail
	if word.find("{")!=-1 or word.find("[")!=-1:
	    bracks=bracks+1
	isthisemail = (isEmail(word))
	if bracks > 0:
	    if(len(word.replace(' ',''))>0):
	        #print word.replace(' ','')+"\t"
	        alp.append((word.replace(' ','')+"\t").encode("utf-8"))
	        alp.append(isthisemail+"\t")
	        alp.append(("0\n").encode("utf-8"))
	        p.append(copy.copy(alp))
	    #print p
	        del alp[:]

	if(len(word.replace(' ',''))>0) and bracks<=0:
	    if (isEmail(word)) == "1":
	        # foutMail.write((word.replace(' ','').strip(',')+"\t").encode("utf-8"))
	        foutMail = foutMail + (word.replace(' ','').strip(',')+"\t").encode("utf-8")
	        # foutMail.write(isthisemail+"\t")
	        foutMail = foutMail + isthisemail+"\t"
	        # foutMail.write(("0\n").encode("utf-8"))
	        foutMail = foutMail + ("0\n").encode("utf-8")
	if word.find("}")!=-1 or word.find("]")!=-1:
	    bracks -= 1
	    if(len(p)!=0):
	        if int(p[len(p)-1][1])==1:              #If it is email
	            for i in range(len(p)):
	                p[i][1] = "1\t"
	        #print p
	        for i in range(len(p)):
	            for j in p[i]:
	                if p[i][1]=="1\t" or p[i][1]=="1":
	                    # foutMail.write(str(j))
	                    foutMail = foutMail + str(j)
	    del p[:]
	return isthisemail


def processStringForMail(string,p,alp,bracks):
	global foutMail
	string = string.strip()
	posAtTheRate = string.find("@")
	if posAtTheRate == -1 or posAtTheRate == 0 or posAtTheRate == len(string)-1:
	    return -1
	string = string.replace("@ ","@").replace(" @","@")
	pe = re.finditer(r'[.] [a-z]', string)
	pe = [m.start() for m in pe]
	sub = 0
	for pos in pe:
	    string = string[:pos-sub+1] + string[pos-sub+2:]
	    sub += 1

	for token in string.split(' '):
	    if processTokenForMail(token,p,alp,bracks) == "1":
	        # foutMail.write("0\t0\t0\n")
	        foutMail = foutMail + "0\t0\t0\n"


def Email_main(root):
	global foutMail
	p = []
	alp = []
	count = 0
	bracks = 0
	count_page = 0
	twotextstaken = False
	for page in root.findall('PAGE'):
	    count_page += 1
	    if count_page > 2:
	        break
	    texts = page.findall('TEXT')
	    iMail = 0
	    stringMail = ""
	    while iMail<len(texts):
	        for tokens in texts[iMail].findall('TOKEN'):
	            if tokens.text is None:
	                #print tokens.text
	                continue
	            if type(tokens.text) is unicode:
	                stringMail += unicodedata.normalize('NFKD', tokens.text).encode('ascii','ignore')
	            else:
	                stringMail += tokens.text
	            stringMail += " "
	        if(twotextstaken == False):
	            twotextstaken = True
	            iMail += 1
	            continue
	        else:
	            #print iMail, stringMail,
	            if processStringForMail(stringMail,p,alp,bracks)!=-1:
	                iMail += 1
	            stringMail = ""
	            twotextstaken = False

	#print foutMail

	################################################################################################################


	flag = "0"   # to check if found the domain (1 => found)
	flag2 = "0"  # to check if we were in a email block (1=>yes) or we have a seperate email (0 => seperate email)
	emails = []
	emails_printed = []
	# filetoRead = directory + "input_mail_parse.txt"
	filetoRead = foutMail
	#outfile = open("/users/user/Desktop/Palod/Allmails.txt",'a')
	#outfile.write("<?" + filetoRead.split("_mail_parse.txt")[0] + "?>\n")
	# with open(filetoRead,'r') as f:
	forMap = ''
	thexml = ''
	lines = filetoRead.split('\n')
	for line in lines:
	    abc = line.split()

	    if len(abc) >= 1:  # if not a blank line

	        if abc[1] == "1":   #output column
	        	if(abc[0].find(":")!=-1):
	        		abc[0] = abc[0].split(":")[1]
			if abc[0].find('{')!=-1 or abc[0].find('[')!=-1:
			    flag2 = "1"
			if abc[0].find('}')==-1 and abc[0].find(']')==-1:
	        	    emails.append((((abc[0].strip('{')).strip('[')).strip(',')))
			if abc[0].find("}")!=-1:
			    domain = str(abc[0].split('}')[len(abc[0].split('}'))-1])
			    for email in ((((abc[0].strip('{')).strip('[')).strip(',')).split('}')[0]).split(','):	#done since there may
			    	emails.append(email)									#not be spaces b/w ,
	        	    flag = "1"
			    flag2 = "0"
			if abc[0].find("]")!=-1:
			    domain = str(abc[0].split(']')[len(abc[0].split(']'))-1])
			    for email in ((((abc[0].strip('{')).strip('[')).strip(',')).split(']')[0]).split(','):
			    	emails.append(email)
	        	    flag = "1"
			    flag2 = "0"
			if flag == "0" and flag2 == "0" and abc[0].lower().find("permissions@acm.")==-1 and abc[0] not in emails_printed:
			    if abc[0].find(",")!=-1:
			    	domain = "@" + abc[0].split("@")[-1]
			    	abc[0] = abc[0].split("@")[0]
			    	for username in abc[0].split(","):
			    		username = username + domain
			    		emails_printed.append(username)
			    		#outfile.write("\n<email>\n\t" + ((((username.strip(',')).strip('.')).strip(')')).strip(',')).strip(';').strip('(') + "\n</email>\n")
			    		thexml += "\n<email>\n\t" + ((((username.strip(',')).strip('.')).strip(')')).strip(',')).strip(';').strip('(') + "\n</email>\n"
			    		forMap += "#e " + ((((username.strip(',')).strip('.')).strip(')')).strip(',')).strip(';').strip('(') + "\n"
			    else:
			    	emails_printed.append(abc[0])
			        #outfile.write("\n<email>\n\t" + ((((abc[0].strip(',')).strip('.')).strip(')')).strip(',')).strip(';').strip('(') + "\n</email>\n")
			        thexml += "\n<email>\n\t" + ((((abc[0].strip(',')).strip('.')).strip(')')).strip(',')).strip(';').strip('(') + "\n</email>\n"
			        forMap += "#e " + ((((abc[0].strip(',')).strip('.')).strip(')')).strip(',')).strip(';').strip('(') + "\n"
			    del emails[:]
			if flag == "1":
			    for usernames in emails:
				if usernames == "":
				    continue
				usernames += domain
				usernames = ((usernames.strip('.')).strip(',')).strip(')').strip('(')
				if usernames not in emails_printed:
				        emails_printed.append(usernames)
				        #outfile.write("\n<email>\n\t" + usernames + "\n</email>\n")
				        thexml += "\n<email>\n\t" + usernames + "\n</email>\n"
				        forMap += "#e " + usernames + "\n"
			    flag = "0"
	        else:
	        	if abc[0] != "0":
	        		flag = "0"
				del emails[:]


	outfile = open(directory + "input_Allmails_for_map_temp.txt",'w')
	outfile.write(forMap)
	outfile.close()
	# print thexml
	# outfile = open(directory+ "input_Allmailsformap.txt",'w')
	# outfile.write(forMap)
	# outfile.close()
	return forMap