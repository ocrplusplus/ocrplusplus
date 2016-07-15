import codecs
import unicodedata

from itertools import izip

def matching_main(names_hash_wala, mails_wali_string):
	directory = '/var/www/html/OCR++/myproject/media/documents/'
	names = ""
	track = 0
	track1 = 0
	#f = open(directory + 'names.txt','w')
	f = ''
	#with open(directory + 'title_author.txt','r') as fi:
	# print names_hash_wala
	# print mails_wali_string
	fi = names_hash_wala.split('\n')
	for line in fi:
		abc = line.split()

		if len(abc) >= 1:
			if abc[0] == "#f":
				track = 0
				names = ""
				names = names + " " + abc[1]
				track = track + 1
			if abc[0] == "#m":
				names = names + " " + abc[1]
				track = track + 1
			if abc[0] == "#l":
				names = names + " " + abc[1]
				track = track + 1
				#f.write("#n " + names + "\n")
				f += names + "\n"

		else:
			#f.write("\n")
			f += "\n"

	#f.close()
	#print names
	#print names
	track = 0
	author = []
	mail = []
	ma = []
	fullmail = []
	found = 0
	maildict = dict(a=1)
	matching_output = "<email_author>\n"
	#print f

	#with open(directory+'names.txt','r') as f1, open(directory+'input_Allmailsformap.txt','r') as f2:
	f1 = names.split('\n')
	f2 = mails_wali_string.split('\n')
	for line1 in f1:
		x = line1.split()
		# y = line2.split()

		if len(x) >= 1:

			# y.remove("#e")

			# fullmail.insert(track,y[0])

			# y1 = y[0].split("@")
			# y1 = y1[0]
			
			uni_x = []
			for it in x:
				it = unicodedata.normalize('NFKD',it.decode("utf-8","ignore")).encode("ascii","ignore")
				uni_x.append(it)
			author.insert(track1,uni_x)

			# mail.insert(track,y[0])
			# ma.insert(track,y[0])
			track1 = track1 + 1


	for line2 in f2:
		y = line2.split()
		if len(y) >= 1:

			# x.remove("#n")
			y.remove("#e")

			fullmail.insert(track,y[0])
			temp = y[0]
			temp.strip()
			temp.strip('(')
			temp.strip('Email:')
			temp.strip(')')
			temp.strip('Id:')
			y1 = y[0].split("@")
			y1 = y1[0]
			y[0] = y[0].replace('_','')
			y1 = y1.replace('_','')
			y[0] = y[0].replace('.','')
			y1 = y1.replace('.','')
			for i in range(10):
				y[0] = y[0].replace(str(i),'')
				y1 = y1.replace(str(i),'')
			# author.insert(track1,x)
			mail.insert(track,y[0].lower())
			ma.insert(track,y[0].lower())
			maildict[y[0].lower()]=temp
			track = track + 1

			# print ma


		# print ma
			#Check if name is a substring of the mail
	# print author
	if len(mail) > 0 and len(author) > 0:
		for mai in ma:
			found = 0
			m = mai.split("@")
			m = m[0]
			# print m
			for a in author:
				l = a
				# print a
				for ao in a:
					ao = ao.replace("-","")
				for n in a:
					# print n
					# print m
					if n.lower() in m:
							matching_output += "\t<map>\n\t\t"
							for na in l:
								matching_output += na
							matching_output += "\n\t\t" + maildict[mai] + "\n"
							matching_output += "\t</map>\n"
							author.remove(l)
							mail.remove(mai)
							found = 1
							break

				if found == 1:
					break

		s = 0
		i = 0
		an = ""
		del ma[:]
		for m in mail:
			ma.insert(s,m)
			s = s + 1
		s = 0

		#Check if every character in mail occurs the same number of time is the name
		if len(mail) > 0 and len(author) > 0:
			for mai in ma:
				m = mai.split("@")
				m = m[0]
				# print m
				for a in author:
					l = a
					for n in a:
						an = an + n
					while s<len(m):
						if m[s] in an.lower():
							if m[s] in an:
								indexx = an.index(m[s])
							else:
								indexx = an.index(m[s].upper())
							s = s + 1
							an = an[0:indexx] + an[indexx+1:]
						else:
							break
					if s == len(m):
						matching_output += "\t<map>\n\t\t"
						for na in l:
							matching_output += na
						matching_output += "\n\t\t" + maildict[mai] + "\n"
						matching_output += "\t</map>\n"
						author.remove(l)
						mail.remove(mai)
					an = ""
					s = 0

				ma[0:] = mail[0:]

				if len(mail) >= 10:
					mail[0:10] = mail[-10:]
					del mail[10:]
					author[0:10] = author[-10:]
					del author[10:]
					ma[0:10] = ma[-10:]
					del ma[10:]
					track = 10

	matching_output += "</email_author>\n"
	#print matching_output
	file_ = open(directory + "map.txt",'w')
	file_.write(matching_output)
	file_.close()
