#####################################################
# Code for mapping email with corresponding author  #
# Author: Barnopriyo Barua                          #
# Email: barno0695@gmail.com                        #
#####################################################

import codecs
import unicodedata
from itertools import izip

#############################
# inputNames format:        #
# #f first name             #
# #m middle name (optional) #
# #l last name              #
#############################

#############################
# inputMails                #
# #e email                  #
#############################

def authorEmailMap(inputNames, inputMails):
	directory = '/var/www/html/OCR++/myproject/media/documents/'
	mapOutputText = "<email_author>\n"

	tempName = ""
	authorNames = ''

	# Generating a string "authorNames" of \n separated names
	for line in inputNames.split('\n'):
		temp = line.split()
		if len(temp) >= 1:
			if temp[0] == "#f":
				tempPos = 0
				tempName = ""
				tempName = tempName + " " + temp[1]
			if temp[0] == "#m":
				tempName = tempName + " " + temp[1]
			if temp[0] == "#l":
				tempName = tempName + " " + temp[1]
				authorNames += tempName.strip() + "\n"
		else:
			authorNames += "\n"

	authorNamesList = authorNames.split('\n')
	emailList = inputMails.split('\n')

	# Normalize author names wherever possible
	# Create an authorList [[first_name,middle_name,last_name],...]
	authorList = []
	for author in authorNamesList:
		tempName = author.split()
		if len(tempName) >= 1:  # Discard names with less than 2 words		
			tempNameList = []
			for word in tempName:
				try:
					word = unicodedata.normalize('NFKD',word.decode("utf-8","ignore")).encode("ascii","ignore")
					tempNameList.append(word)
				except:
					print "ERROR: Normalization error"
			authorList.append(tempNameList)
			tempPos = tempPos + 1

	emailListCharRemoved = []
	tempEmailListCharRemoved = []

	# Generating a dict "mailDict" mapping email with special chars and digits removed(except @) to actual email
	mailDict = {}
	for email in emailList:
		email = email.split()

		# Discarding junk lines
		if len(email) < 1:
			continue

		email = email[1] # Removing #e
		tempEmail = email
		email.strip()
		email.strip('(')
		email.strip('Email:')
		email.strip(')')
		email.strip('Id:')

		# Removing special chars and digits
		tempEmail = tempEmail.replace('_','')
		tempEmail = tempEmail.replace('.','')
		for i in range(10):
			tempEmail = tempEmail.replace(str(i),'')

		emailListCharRemoved.append(tempEmail.lower())
		tempEmailListCharRemoved.append(tempEmail.lower())
		mailDict[tempEmail.lower()] = email

	if len(emailListCharRemoved) > 0 and len(authorList) > 0:
		found = 0
		# Checking if name is a substring of the email username
		for email in tempEmailListCharRemoved:
			found = 0
			user = email.split("@")[0]
			for author in authorList:
				tempAuthor = author
				for word in author:
					word = word.replace("-","")
					if word.lower() in user:
							mapOutputText += "\t<map>\n\t\t"
							for tempWord in tempAuthor:
								mapOutputText += tempWord + " "
							mapOutputText += "\n\t\t" + mailDict[email] + "\n"
							mapOutputText += "\t</map>\n"
							authorList.remove(tempAuthor)
							emailListCharRemoved.remove(email)
							found = 1
							break
				if found == 1:
					break

		del tempEmailListCharRemoved[:]
		for email in emailListCharRemoved:
			tempEmailListCharRemoved.append(email)

		# Checking if every character in email username occurs the same number of times as in the author's name
		tempAuthorName = ""
		tempPos = 0
		if len(emailListCharRemoved) > 0 and len(authorList) > 0:
			for email in tempEmailListCharRemoved:
				user = email.split("@")[0]
				for author in authorList:
					tempAuthor = author
					for word in author:
						tempAuthorName = tempAuthorName + word
					while tempPos<len(user):
						if user[tempPos] in tempAuthorName.lower():
							if user[tempPos] in tempAuthorName:
								index = tempAuthorName.index(user[tempPos])
							else:
								index = tempAuthorName.index(user[tempPos].upper())
							tempPos = tempPos + 1
							tempAuthorName = tempAuthorName[0:index] + tempAuthorName[index+1:]
						else:
							break
					if tempPos == len(user):
						mapOutputText += "\t<map>\n\t\t"
						for word in tempAuthor:
							mapOutputText += word + " "
						mapOutputText += "\n\t\t" + mailDict[email] + "\n"
						mapOutputText += "\t</map>\n"
						authorList.remove(tempAuthor)
						emailListCharRemoved.remove(email)
					tempAuthorName = ""
					tempPos = 0

	mapOutputText += "</email_author>\n"
	file_ = open(directory + "map.txt",'w')
	file_.write(mapOutputText)
	file_.close()
