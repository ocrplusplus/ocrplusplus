#####################################################
# Code for extracting and printing author names     #
# Author: Barnopriyo Barua                          #
# Email: barno0695@gmail.com                        #
#####################################################

import nltk
import unicodedata
import subprocess
import xml.etree.ElementTree as ET

country_list = ["City", "America", "UK", "Afghanistan", "Albania", "Algeria", "Samoa", "Andorra", "Angola", "Anguilla",
                "Barbuda", "Argentina", "Armenia", "Aruba", "San Diego", "San Francisco", "Australia", "Austria",
                "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin",
                "Bermuda", "Bhutan", "Bolivia", "Herzegowina", "Botswana", "Island", "Brazil", "Brunei", "Bulgaria",
                "Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Canada", "Cape Verde", "Chad", "Chile", "China",
                "Colombia", "Comoros", "Congo", "Costa Rica", "Ivoire", "Croatia", "Cuba", "Cyprus", "Denmark",
                "Djibouti", "Timor", "Ecuador", "Egypt", "Salvador", "Guinea", "Eritrea", "Estonia", "Ethiopia", "Fiji",
                "Finland", "France", "Territories", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Gibraltar",
                "Greece", "Grenada", "Guadeloupe", "Guam", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti",
                "Honduras", "Kong", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel",
                "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea", "Kuwait",
                "Kyrgyzstan", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania",
                "Luxembourg", "Macau", "Macedonia", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta",
                "Martinique", "Mauritania", "Mauritius", "Mayotte", "Mexico", "Micronesia", "Moldova", "Monaco",
                "Mongolia", "Montserrat", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal",
                "Netherlands", "New Caledonia", "New Zealand", "Nicaragua", "Niger", "Nigeria", "Niue", "Norway",
                "Oman", "Pakistan", "Palau", "Panama", "Paraguay", "Peru", "Philippines", "Pitcairn", "Poland",
                "Portugal", "Rico", "Qatar", "Romania", "Russia", "Federation", "Rwanda", "Samoa", "Arabia", "Senegal",
                "Seychelles", "Singapore", "Slovakia", "Slovenia", "Islands", "Somalia", "South Africa", "Spain",
                "Lanka", "Helena", "Miquelon", "Sudan", "Suriname", "Swaziland", "Sweden", "Switzerland", "Taiwan",
                "Tajikistan", "Tanzania", "Thailand", "Togo", "Tokelau", "Tonga", "Tobago", "Tunisia", "Turkey",
                "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "Emirates", "Kingdom", "States", "Uruguay", "USA", "UAE",
                "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Yemen", "Yugoslavia", "Zambia", "Zimbabwe"]

US_States = ["Los Angeles", "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut",
             "Delaware", "Columbia", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas",
             "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
             "Missouri", "Montana", "Nebraska", "Nevada", "Hampshire", "Jersey", "York", "Carolina", "Dakota", "Ohio",
             "Oklahoma", "Oregon", "Pennsylvania", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
             "Wisconsin", "Wyoming"]

Exceptional_names = ["MSN", "IIT", "KU Leuven", "INSEAD", "ESCP Europe", "Sciences Po Paris", "ETH Zurich", "EPFL",
                     "HKUST", "CAIDA", "BITS", "UC Berkeley", "Facebook", "Google", "Amazon", "Twitter", "MIT",
                     "TU Delft"]

journal_related = ["Theory", "Comput", "Machine", "Network", "System", "Member", "Computer", "Medical", "Society",
                   "Conference", "Copyright", "Journal ", "JOURNAL", "ACM", "Elsevier", "ELSEVIER", "arxiv", "ARXIV",
                   "IEEE", "ieee", "Grant", "GRANT", "grant", "CONFERENCE", "INTERNATIONAL", "R E S E A R C H",
                   "RESEARCH", "DETECTION", "Detection", "Open", "International"]

SectionHeads = ["Abstract", "ABSTRACT", "Introduction", "INTRODUCTION", "REFERENCES", "ARTICLE"]


# RUN THIS BEFORE CALLING PRINTAUTH
# crf_test -m $Directory/files/model_all_com.txt $Directory/test_aut.txt > $Directory/final_aut.txt

# If aut is in title
def checkintitle(aut, title):
    if aut in title:
        return 1
    return 0

# If aut is in affiliation
def checkinaffil(aut, input_AllAff):
    if aut in input_AllAff:
        return 1
    return 0


def printAuthor(title_xml, input_Affl):
    subprocess.call("crf_test -m model_all_com.txt test_aut.txt > final_aut.txt", shell=True)
    directory = '/var/www/html/OCR++/myproject/media/documents/'

    flag = "0"  # to check if a title is already going on
    end = 0
    titl = 0;
    affils = []
    auts = []
    input_Affl = ET.tostring(input_Affl)
    aff_lines = input_Affl.split('\n')
    for line in aff_lines:
        if "Affiliation" in line:
            continue
        line = line.strip('\t')
        line = line.strip('\n')
        affils.append(line)

    fout = title_xml

    tokenss = []
    titl_done = 0
    tokens = 0
    caps = 0
    name = ""
    cont = 0
    pending_names = []
    ex_y = 0
    flagy = 0
    flagx = 0
    namerem = ""
    ex_x = 0
    ex_w = 0
    authoraya = 0
    with open(directory + 'final_aut.txt', 'r') as f:
        for line in f:
            # print lineno
            # lineno = lineno + 1
            abc = line.split()

            if len(abc) > 1:
                # print "yo1"
                # print "***" + abc[0]
                abc[0] = abc[0].replace('&', '&amp;')
                tokenss.append(abc[0])


                if int(abc[12]) != 0 or int(abc[13]) != 0:
                    # print abc[9]
                    # print abc[12]
                    if abc[0] != ',':
                        # print float(abc[9]) - (ex_x + ex_w)
                        if float(abc[9]) - (ex_x + ex_w) <= 10 and ex_y == float(abc[8]):
                            # if flagx==0:
                            # 	flagx = 1
                            # print abc[0]
                            ex_x = float(abc[9])
                            ex_w = float(abc[10])
                            ex_y = float(abc[8])
                            name = name + abc[0] + " "
                            # print "name " + name
                            continue
                        else:
                            flagx = 0
                            namerem = abc[0] + " "
                else:
                    flagx = 0


                if len(name.split()) > 0:
                    # print "yo2"
                    for a in affils[1:]:
                        # a = a.strip('.')
                        # print a
                        # print name.replace('.','')
                        if a in name.replace('.', ''):
                            # print "yo"
                            if len(a.split()) > 0:

                                name = name.replace('.', '')
                                # print name
                                pending_names.append(name.split(a)[0])
                                if len(name.split(a)) > 0:
                                    name = name.split(a)[1]
                                # name = names.split(a)[0]
                                # name = name.replace(a,'')

                    if name not in pending_names:
                        pending_names.append(name)
                    # print pending_names

                    for name in pending_names:
                        name = name.replace('*', '')
                        remove = 0
                        for country in country_list:
                            if country in name:
                                remove = 1
                        for Exceptional in Exceptional_names:
                            if Exceptional in name:
                                remove = 1
                        for states in US_States:
                            if states in name:
                                remove = 1
                        for journal in journal_related:
                            if journal in name:
                                remove = 1
                        for head in SectionHeads:
                            if head in name:
                                remove = 1
                        # print name
                        if len(name) > 1 and name[
                            0].isupper() and remove == 0 and "Corporat" not in name and "Academ" not in name and "The " not in name and "Normale" not in name and "Universit" not in name and "Research" not in name and "Polytechnique" not in name and "Technolog" not in name and "Politecnic" not in name and "Univ." not in name and "Universidad" not in name and "Ecole" not in name and "Cntr." not in name and "Institut" not in name and "Centre" not in name and "Department" not in name and "School" not in name and "College" not in name and "Lab" not in name and "Labs" not in name and "Laborator" not in name and "Dept." not in name and "faculty" not in name and "Technologies" not in name and "Inc." not in name:
                            # print name
                            tag = nltk.pos_tag(
                                unicodedata.normalize('NFKD', unicode(name, 'utf8')).encode('ascii', 'ignore').split())
                            # print tag
                            propernoun = [word for word, pos in tag if pos == 'NNP' or pos == "NN" or pos == "NP"]

                            if len(propernoun) == len(name.split()):
                                name = name.replace(',', '')
                                name = name.replace('(', '')
                                name = name.replace(')', '')
                                name = name.strip()
                                if unicodedata.normalize('NFKD', unicode(name, 'utf8')).encode('ascii', 'ignore')[
                                    -1].isdigit():
                                    name = unicodedata.normalize('NFKD', unicode(name, 'utf8')).encode('ascii', 'ignore')[
                                           0:-1]
                                names = name.split()
                                # print name
                                singl = 0
                                for n in names:
                                    if len(n) > 1:
                                        singl = 1
                                if checkintitle(name, title_xml) == 0 and checkinaffil(
                                        name, input_Affl) == 0 and name not in auts and unicodedata.normalize('NFKD', unicode(
                                        name.replace(' ', '').replace('.', '').replace('-', ''), 'utf8')).encode('ascii',
                                                                                                                 'ignore').isalpha() and \
                                                names[0] != names[-1] and len(names) < 5 and singl == 1:
                                    auts.append(name)
                                    authoraya = 1
                                    wrt = "\t<name>\n"
                                    wrt = wrt + "\t\t<first_name>\n"
                                    wrt = wrt + "\t\t\t" + names[0] + "\n"
                                    wrt = wrt + "\t\t</first_name>\n"
                                    if len(names) > 2:
                                        # print len(name)
                                        wrt = wrt + "\t\t<middle_name>\n"
                                        wrt = wrt + "\t\t\t"
                                        for n in names[1:-1]:
                                            wrt = wrt + n + " "
                                        wrt = wrt + "\n"
                                        wrt = wrt + "\t\t</middle_name>\n"
                                    wrt = wrt + "\t\t<last_name>\n"
                                    wrt = wrt + "\t\t\t" + names[-1] + "\n"
                                    wrt = wrt + "\t\t</last_name>\n"
                                    wrt = wrt + "\t</name>\n\n"
                                    # fout.write(wrt)
                                    fout += wrt
                            name = ""

                            if len(pending_names) > 0:
                                pending_names = []
                                ex_x = float(abc[9])
                                ex_w = float(abc[10])
                                ex_y = float(abc[8])
                                continue

                            # print name
                            tag = nltk.pos_tag(
                                unicodedata.normalize('NFKD', unicode(name, 'utf8')).encode('ascii', 'ignore').split())
                            propernoun = [word for word, pos in tag if pos == 'NNP']
                            name = name.strip()
                            if unicodedata.normalize('NFKD', unicode(name, 'utf8')).encode('ascii', 'ignore')[-1].isdigit():
                                name = unicodedata.normalize('NFKD', unicode(name, 'utf8')).encode('ascii', 'ignore')[0:-1]
                            if checkintitle(name, title_xml) == 0 and checkinaffil(name, input_Affl) == 0 and len(propernoun) == len(
                                    name.split()) and name not in auts and unicodedata.normalize('NFKD', unicode(
                                    name.replace(' ', '').replace('.', '').replace('-', ''), 'utf8')).encode('ascii',
                                                                                                             'ignore').isalpha():
                                auts.append(name)
                                name = name.split()
                                # print name
                                authoraya = 1
                                wrt = "\t<name>\n"
                                wrt = wrt + "\t\t<first_name>\n"
                                wrt = wrt + "\t\t\t" + name[0] + "\n"
                                wrt = wrt + "\t\t</first_name>\n"
                                if len(name) > 2:
                                    # print len(name)
                                    wrt = wrt + "\t\t<middle_name>\n"
                                    wrt = wrt + "\t\t\t"
                                    for n in name[1:-1]:
                                        wrt = wrt + n + " "
                                    wrt = wrt + "\n"
                                    wrt = wrt + "\t\t</middle_name>\n"
                                wrt = wrt + "\t\t<last_name>\n"
                                wrt = wrt + "\t\t\t" + name[-1] + "\n"
                                wrt = wrt + "\t\t</last_name>\n"
                                wrt = wrt + "\t</name>\n\n"
                                # fout.write(wrt)
                                fout += wrt

                # print "aayayayaya"
                name = namerem
                namerem = ""
                ex_x = float(abc[9])
                ex_w = float(abc[10])
                ex_y = float(abc[8])
            # print "name" + name

    autrun = 1
    aut = ""
    if authoraya == 0 or authoraya == 1:
        pending_names = []
        for i in range(0, len(tokenss)):
            # print tokenss[i]
            # print autrun
            if autrun == 0:
                if tokenss[i][0].isdigit() or tokenss[i][0] == ',' or tokenss[i][0] == 'and':
                    aut = ""
                    autrun = 1
                # aut = aut + t[i] + " "
            else:
                if tokenss[i][0].isdigit() or tokenss[i][0] == ',' or tokenss[i][0] == '*' or tokenss[i][0].islower():

                    pending_names.append(aut)
                    aut = ""
                    autrun = 1
                else:
                    aut = aut + tokenss[i] + " "

        # print pending_names

        for name in pending_names:
            name = name.replace('*', '')
            remove = 0
            for country in country_list:
                if country in name:
                    remove = 1
            for Exceptional in Exceptional_names:
                if Exceptional in name:
                    remove = 1
            for states in US_States:
                if states in name:
                    remove = 1
            for journal in journal_related:
                if journal in name:
                    remove = 1
            for head in SectionHeads:
                if head in name:
                    remove = 1
            # print name
            name = name.strip()

            if len(name) > 1 and unicodedata.normalize('NFKD',
                                                       unicode(name.replace(' ', '').replace('.', '').replace('-', ''),
                                                               'utf8')).encode('ascii', 'ignore').isalpha() and name[
                0].isupper() and remove == 0 and "Corporat" not in name and "Academ" not in name and "The " not in name and "Normale" not in name and "Universit" not in name and "Research" not in name and "Polytechnique" not in name and "Technolog" not in name and "Politecnic" not in name and "Univ." not in name and "Universidad" not in name and "Ecole" not in name and "Cntr." not in name and "Institut" not in name and "Centre" not in name and "Department" not in name and "School" not in name and "College" not in name and "Lab" not in name and "Labs" not in name and "Laborator" not in name and "Dept." not in name and "faculty" not in name and "Technologies" not in name and "Inc." not in name:
                # print name
                tag = nltk.pos_tag(unicodedata.normalize('NFKD', unicode(name, 'utf8')).encode('ascii', 'ignore').split())
                # print tag
                propernoun = [word for word, pos in tag if pos == 'NNP' or pos == "NN" or pos == "NP"]

                if len(propernoun) == len(name.split()):
                    name = name.replace(',', '')
                    name = name.replace('(', '')
                    name = name.replace(')', '')
                    # print name[-1]
                    if unicodedata.normalize('NFKD', unicode(name, 'utf8')).encode('ascii', 'ignore')[-1].isdigit():
                        name = unicodedata.normalize('NFKD', unicode(name, 'utf8')).encode('ascii', 'ignore')[0:-1]
                    names = name.split()
                    # print name
                    singl = 0
                    for n in names:
                        if len(n) > 1:
                            singl = 1
                    if checkintitle(name,title_xml) == 0 and checkinaffil(name, input_Affl) == 0 and name not in auts and unicodedata.normalize(
                            'NFKD', unicode(name.replace(' ', '').replace('.', '').replace('-', ''), 'utf8')).encode(
                            'ascii', 'ignore').isalpha() and names[0] != names[-1] and len(names) < 3 and singl == 1:
                        auts.append(name)
                        authoraya = 1
                        wrt = "\t<name>\n"
                        wrt = wrt + "\t\t<first_name>\n"
                        wrt = wrt + "\t\t\t" + names[0] + "\n"
                        wrt = wrt + "\t\t</first_name>\n"
                        if len(names) > 2:
                            # print len(name)
                            wrt = wrt + "\t\t<middle_name>\n"
                            wrt = wrt + "\t\t\t"
                            for n in names[1:-1]:
                                wrt = wrt + n + " "
                            wrt = wrt + "\n"
                            wrt = wrt + "\t\t</middle_name>\n"
                        wrt = wrt + "\t\t<last_name>\n"
                        wrt = wrt + "\t\t\t" + names[-1] + "\n"
                        wrt = wrt + "\t\t</last_name>\n"
                        wrt = wrt + "\t</name>\n\n"
                        # fout.write(wrt)
                        fout += wrt
                name = ""


    # fout.close()

    fout += "</title_author>"
    fileTitAut = open(directory + "TitleAuthor.xml",'w')
    fileTitAut.write(fout)
    return fout


#printAuthor("<?xml version=\"1.0\" ?>\n<title_author>\n\t<title>\n\tOptimizing Panchromatic Image Change Detection Based on Change Index Multiband Image Analysis\n	</title>\n\t</title_author>", "<Affiliation>\nE Martinez Universidad Politecnica de Madrid Espana\n</Affiliation>\n<Affiliation>\nA Arquero Universidad Politecnica de Madrid Espana\n</Affiliation>\n<Affiliation>\nI Molina Universidad Politecnica de Madrid Espana\n</Affiliation>")