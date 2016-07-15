import xml.etree.ElementTree as ET
directory= '/var/www/html/OCR++/myproject/media/documents/'

f = open(directory + "input_Allmails_for_map_temp.txt",'r')
out = open(directory + 'eval_emails.txt','w')
emails = f.readlines()
for mail in emails:
	out.write(mail.replace('#e ','<<Email>> \n').strip())
f.close()
out.close()