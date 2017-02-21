# __author__ = "barno"
import xml.etree.ElementTree as ET
import os.path
import subprocess


def binary(x):
    if x == "yes":
        return "1"
    return "0"


def startCaps(y):
    x = y.strip()
    if x[0].isupper():
        return "1"
    else:
        return "0"


def comma(y):
    x = y.strip()
    if x[len(x) - 1] == ',':
        return "1"
    else:
        return "0"


def commonwords(y):
    x = y.strip()
    if x == "The" or x == "and" or x == "of" or x == "Student" or x == "Senior" or x == "Junior" or x == "Member":
        return "1"
    else:
        return "0"


# 2nd Comma
# def comma(y):
#     x = y.strip()
#     if x[len(x) - 1] == ',':
#         return "1"
#     else:
#         return "0"

def TitleAuthor_parse(root,input_AllAffiliations):
    directory = '/var/www/html/OCR++/myproject/media/documents/'
    #tree = ET.parse(directory + 'input.xml')
    #root = tree.getroot()
    l = 0
    if os.path.exists(directory + 'eval_Secmap.txt'):
        with open(directory + 'eval_Secmap.txt', 'r') as f:
            for line in f:
                l = l + 1

    # print l
    first_chunk = ""
    if l > 1:
        sectree = ET.parse(directory + 'Secmap.xml')
        secroot = sectree.getroot()
        flag = 0
        # first_chunk = ""
        # print "yo"
        # for secmap in secroot.findall('sec_map'):
        #	 print "yo"
        for secs in secroot.findall('section'):
            # print "yo"
            for chunk in secs.findall('chunk'):
                # print "yo"
                first_chunk = chunk.text.replace(' ', '')
                # print first_chunk
                break
            break
            # break

    # print "f " + first_chunk




    # def comma(y):
    #	 x = y.strip()
    #	 if x[len(x)-1] == ',':
    #		 return "1"
    #	 else:
    #		 return "0"

    temp = first_chunk

    # print "titleauthorparse starting"
    # To find max font size and total number to textxs in the file
    page = 0
    max_fs = 0
    tot_txt_chunk = 0
    tot_txt = 0
    chunk_over = 0
    for pages in root.findall('PAGE'):
        page = page + 1
        for texts in pages.findall('TEXT'):
            if chunk_over == 0:
                tot_txt_chunk = tot_txt_chunk + 1
            tot_txt = tot_txt + 1
            for token in texts.findall('TOKEN'):
                if token.text is None:
                    continue

                word = token.text

                word = word.replace(' ', '')

                # print word
                if word == first_chunk[:len(word)]:
                    first_chunk = first_chunk[len(word):]
                if len(first_chunk) == 0:
                    chunk_over = 1

                if (float(token.attrib['font-size']) > max_fs):
                    # print token.text
                    # if chunk_over == 0:
                    max_fs = float(token.attrib['font-size'])

                    #	 if chunk_over == 1:
                    #		 break
                    # if chunk_over == 1:
                    #	 break

    # f = open(directory + 'test.txt','w')
    f = ""
    # f.write("0\t0\t0\t0\t0\t0\n")

    first_chunk = temp

    # print first_chunk

    # print "***"
    # print tot_txt
    flagg = 0
    txt = 0
    count = 0
    chunk_over = 0
    for pages in root.findall('PAGE'):
        count = count + 1
        if count > 2:  # Only first two pages to search
            break
        for texts in pages.findall('TEXT'):

            txt = txt + 1
            for token in texts.findall('TOKEN'):
                if token.text is None:
                    continue

                # if type(token.text) is unicode:
                # 	word = unicodedata.normalize('NFKD', token.text).encode('ascii','ignore')
                # else:
                word = token.text

                word = word.replace(' ', '')

                # print word
                # print len(first_chunk)
                if word == first_chunk[:len(word)]:
                    first_chunk = first_chunk[len(word):]
                if len(first_chunk) == 0:
                    chunk_over = 1

                if (len(word) > 0):
                    # print "----------"
                    # print txt
                    # print tot_txt_chunk
                    # print "----------"
                    f = f + (word + "\t").encode("utf-8")
                    f = f + (binary(token.attrib['bold']) + "\t").encode("utf-8")
                    f = f + (str(round(float(txt) / (tot_txt), 2)) + "\t").encode("utf-8")
                    if float(txt) > tot_txt_chunk:
                        f = f + "0\t"
                    else:
                        f = f + (str(round(float(txt) / (tot_txt_chunk), 2)) + "\t").encode("utf-8")
                    if max_fs != 0:
                        f = f + (str(round(float(token.attrib['font-size']) / (max_fs), 2)) + "\t").encode("utf-8")
                    else:
                        f = f + "00\t"
                    f = f + (startCaps(token.text.encode("utf-8").replace(' ', ''))) + "\t"
                    f = f + (comma(token.text.encode("utf-8").replace(' ', ''))) + "\t"
                    f = f + (commonwords(token.text.encode("utf-8").replace(' ', ''))) + "\t"
                    f = f + (str(token.attrib['y']) + "\t").encode("utf-8")
                    f = f + (str(token.attrib['x']) + "\t").encode("utf-8")
                    f = f + (str(token.attrib['width']) + "\t").encode("utf-8")
                    f = f + ("0\n").encode("utf-8")

            f = f + "00\t00\t00\t00\t00\t00\t00\t00\t00\t00\t00\t00\n"
            if chunk_over == 1 and l > 1:
                break
        if chunk_over == 1 and l > 1:
            break

    f = f + "00\t00\t00\t00\t00\t00\t00\t00\t00\t00\t00\t00"

    # f.close()
    # print f

    ##################################################################################################################


    # directory = ''


    fi = open(directory + 'test_file.txt', 'w')

    fs = ''

    # flag = "0"   # to check if a title is already going on
    end = 0

    # with open(directory + 'test.txt','r') as f:
    lines = f.split('\n')
    for line in lines:
        abc = line.split()

        if len(abc) == 12:  # if not a blank line

            if abc[4] == fs:
                l = abc[0] + "\t" + abc[1] + "\t" + abc[2] + "\t" + abc[3] + "\t" + abc[4] + "\t" + abc[5] + "\t" + abc[
                    6] + "\t" + abc[7] + "\t" + abc[8] + "\t" + abc[9] + "\t" + abc[10] + "\t" + abc[11] + "\n"
            else:
                fs = abc[4]
                l = "00\t00\t00\t00\t00\t00\t00\t00\t00\t00\t00\t00\n"
                l = l + abc[0] + "\t" + abc[1] + "\t" + abc[2] + "\t" + abc[3] + "\t" + abc[4] + "\t" + abc[5] + "\t" + \
                    abc[
                        6] + "\t" + abc[7] + "\t" + abc[8] + "\t" + abc[9] + "\t" + abc[10] + "\t" + abc[11] + "\n"

            fi.write(l)

    fi.close()

    subprocess.call("crf_test -m ./model_all_com.txt ./test_file.txt > ./final.txt", shell=True)

    directory = ''

    fs = ''

    inputfile = []

    titlecount = 0
    authorcount = 0
    maxfs = 0

    # flag = "0"  # to check if a title is already going on
    # end = 0


    with open(directory + 'final.txt', 'r') as f:
        for line in f:
            abc = line.split()

            if len(abc) > 1:  # if not a blank line
                if float(abc[4]) > maxfs:
                    maxfs = float(abc[4])
                inputfile.append(abc)
                if abc[12] == '1':
                    titlecount = titlecount + 1
                if abc[12] == '2':
                    authorcount = authorcount + 1

    if titlecount == 0:
        fi = open(directory + 'final.txt', 'w+')
        # print len(inputfile)
        fi.seek(0)
        l = ""
        for abc in inputfile:
            if float(abc[4]) == maxfs:
                # print "yo"
                l = abc[0] + "\t" + abc[1] + "\t" + abc[2] + "\t" + abc[3] + "\t" + abc[4] + "\t" + abc[5] + "\t" + abc[
                    6] + "\t" + abc[7] + "\t" + abc[8] + "\t" + abc[9] + "\t" + abc[10] + "\t" + abc[11] + "\t1\n"
            else:
                l = abc[0] + "\t" + abc[1] + "\t" + abc[2] + "\t" + abc[3] + "\t" + abc[4] + "\t" + abc[5] + "\t" + abc[
                    6] + "\t" + abc[7] + "\t" + abc[8] + "\t" + abc[9] + "\t" + abc[10] + "\t" + abc[11] + "\t" + abc[
                        12] + "\n"

            fi.write(l)
        fi.truncate()
        fi.close()

    #######################################################################

    directory = ''

    flag = "0"  # to check if a title is already going on
    end = 0
    titl = 0
    fi = open(directory + 'test_aut.txt', 'w')
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

    final_lines = []

    with open(directory + 'final.txt', 'r') as f:
        # final_lines = f.readlines()
        for line in f:
            # global final_lines
            final_lines.append(line)
            abc = line.split()
            # print "asdasd"
            if len(abc) > 1:  # if not a blank line
                if float(abc[4]) > maxsize:
                    secmaxsize = maxsize
                    maxsize = float(abc[4])

                if float(abc[4]) > secmaxsize and float(abc[4]) < maxsize:
                    secmaxsize = float(abc[4])
                # print "***" + abc[0]
                abc[0] = abc[0].replace('&', '&amp;')

                # if(abc[9]=="00"):
                # 	print

                if abc[0] == "00":
                    # titl_done = 1
                    continue
                temp = abc[0]
                lines.append(line)
                if titl_done == 0:
                    if abc[12] == "1":  # output column
                        # print "aaaa"
                        titl = 1
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
                        if float(abc[4]) > maxsz:
                            maxsz = float(abc[4])
                        sizes.append(abc[4])
                        # print "here1"
                        titl_ext = titl_ext + abc[0] + " "
                        flag = "1"
                        fi.write(line)
                    else:
                        if abc[0] != "0" and flag == "1":
                            if (titl == 1):
                                # print("\n\t</title>")
                                # if titllen > 10:
                                titl_done = 1
                                possible_titles.append(titl_ext)
                                titl_ext = ""
                                pos.append(relpos)
                                size.append(relsize)
                                titl = 0;
                                if lineno == 1 and abc[0] == temp:
                                    k = 1
                                else:
                                    # print "yo"
                                    if ex_y != float(abc[8]):
                                        fi.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
                                    if ',' in abc[0]:
                                        for a in abc[:-1]:
                                            fi.write(a.replace(',', '') + "\t")
                                        fi.write(abc[-1] + "\n,\t")
                                        for a in abc[1:-1]:
                                            fi.write(a.replace(',', '') + "\t")
                                        fi.write(abc[-1] + "\n")
                                    else:
                                        fi.write(line)
                                lineno = lineno + 1
                            # print "here2"
                            flag = "0"

                            # print

                    if abc[12] == "2":  # first name
                        if (titl == 1):
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
                        if lineno == 1 and abc[0] == temp:
                            k = 1
                        else:
                            if ex_y != float(abc[8]):
                                fi.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
                            if ',' in abc[0]:
                                for a in abc[:-1]:
                                    fi.write(a.replace(',', '') + "\t")
                                fi.write(abc[-1] + "\n,\t")
                                for a in abc[1:-1]:
                                    fi.write(a.replace(',', '') + "\t")
                                fi.write(abc[-1] + "\n")
                            else:
                                fi.write(line)
                        lineno = lineno + 1
                else:
                    if abc[12] == '1':
                        relpos = abc[3]
                        relsize = abc[4]
                        if float(abc[4]) > maxsz:
                            maxsz = float(abc[4])
                        sizes.append(abc[4])
                        #print "ssss"
                        titl_ext = titl_ext + abc[0] + " "

                    if ',' in abc[0]:
                        if len(abc[0]) > 1:
                            line = line.strip(abc[0])
                            abc[0] = abc[0].strip(',')
                            line = abc[0] + line + ',' + line

                    if ex_y != float(abc[8]):
                        fi.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
                    if ',' in abc[0]:
                        for a in abc[:-1]:
                            fi.write(a.replace(',', '') + "\t")
                        fi.write(abc[-1] + "\n,\t")
                        for a in abc[1:-1]:
                            fi.write(a.replace(',', '') + "\t")
                        fi.write(abc[-1] + "\n")
                    else:
                        fi.write(line)
                    if abc[0] != '00':
                        tokens = tokens + 1
                    if tokens >= 120:
                        break
                ex_y = float(abc[8])

    fi.close()

    if len(titl_ext) < 6:
        with open(directory + 'test_aut.txt', 'w') as fia:
            no = 0
            for line in lines:
                abc = line.split()
                if ex_y != float(abc[8]):
                    fia.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
                if ',' in abc[0]:
                    for a in abc[:-1]:
                        fia.write(a.replace(',', '') + "\t")
                    fia.write(abc[-1] + "\n,\t")
                    for a in abc[1:-1]:
                        fia.write(a + "\t")
                    fia.write(abc[-1] + "\n")
                else:
                    fia.write(line)
                # fia.write("\n")
                no = no + 1
                if no == 120:
                    # fia.close()
                    break
                ex_y = float(abc[8])
                # fia.close()

    tlt = ""
    for tt in possible_titles:
        ttt = tt.split()
        for tt in ttt:
            tlt = tlt + tt + " "
    tlt = tlt + titl_ext

    if len(sizes) == len(tlt.split()) and len(sizes) > 0:
        # print "yo"
        tempt = tlt.split()
        titl_ext = ""
        for i in range(0, len(sizes)):
            if float(sizes[i]) == maxsz:
                titl_ext = titl_ext + tempt[i] + " "

    # print titl_ext + "-----------"
    possible_titles = []
    possible_titles.append(titl_ext)
    pos.append(relpos)
    size.append(relsize)
    titl_ext = ""

    it = []
    # print(possible_titles)
    for i in range(0, len(possible_titles)):
        # print "Blah"
        # print i
        # print possible_titles[i].split()
        if len(possible_titles[i].split()) > 0 and len(possible_titles[i].split()) <= 25:
            it.append(i)
            # print i

    if len(it) == 0:
        possible_titles.append('S')
        pos.append('0.5')
        size.append('0.5')
        it.append(1)

    lpos = it[0]   
    msize = it[0]
    for i in it:
        if float(pos[lpos]) > float(pos[i]):
            lpos = i
        if float(size[msize]) < float(size[i]):
            msize = i

    fi = []

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
        for i in range(0, len(it)):
            # if len(titl_ext.split())<=225:
            titl_ext = titl_ext + possible_titles[i] + " "

    for l in lines:
        if "arXiv:" in l:
            tx = ""
            arx = 1

    if arx == 1 or len(titl_ext.split()) < 2:
        titl_ext = ""
        # with open(directory + 'final.txt', 'r') as f:
        for line in final_lines:
            abc = line.split()

            if len(abc) > 1:
                # print secmaxsize
                if float(abc[4]) == secmaxsize:
                    # if len(titl_ext) <= 225:
                    # print abc[0]
                    titl_ext = titl_ext + abc[0] + " "

    affils = []

    ######################### TAKE STRING
    # with open(directory + 'input_AllAffiliations.txt', 'r') as f:
    #####################################

    '''
    Aff_lines = input_AllAffiliations.split('\n')
    for line in Aff_lines:
        if "Affiliation" in line:
            continue
        line = line.strip('\t')
        line = line.strip('\n')
        affils.append(line)
    '''
    for aff in input_AllAffiliations.findall('Affiliation'):
        affils.append(aff.text)
    # print titl_ext
    for a in affils:
        if a in titl_ext:
            titl_ext = titl_ext.replace(a, '')

    if "Conference" in titl_ext or "IEEE" in titl_ext or "ACM" in titl_ext or "JOURNAL" in titl_ext or "Journal" in titl_ext:
        titl_ext = ""

    if len(titl_ext) < 5 or titl_ext == "Case study ":
        # print maxsize
        # print "yo"
        # with open(directory + 'final.txt', 'r') as f:
        for line in final_lines:
            abc = line.split()

            if len(abc) > 1:
                if float(abc[4]) == maxsize:
                    titl_ext = titl_ext + abc[0] + " "

    wrds = titl_ext.split()
    if len(wrds) > 25:
        titl_ext = ""
        for i in range(0, 25):
            titl_ext = titl_ext + wrds[i] + " "

    # print possible_titles

    wrds = titl_ext.split()
    if ''.join([i for i in wrds[0] if not i.isdigit()]).isupper() and ''.join(
            [i for i in wrds[1] if not i.isdigit()]).isupper() and ''.join(
            [i for i in wrds[2] if not i.isdigit()]).isupper():
        titl_ext = ""
        for w in wrds:
            if not ''.join([i for i in w if not i.isdigit()]).isupper():
                break
            titl_ext = titl_ext + w + " "

    # temp = open(directory + 'temptitle.txt','w')
    # temp.write(titl_ext)
    # temp.close()

    temp_title = titl_ext

    titl_ext = "<?xml version=\"1.0\" ?>\n<title_author>\n\t<title>\n\t" + titl_ext
    #print titl_ext
    #print "\n\t</title>"
    # print("</title_author>\n")
    return titl_ext+"\n\t</title>"


# TitleAuthor_parse("<Affiliation>E Martinez Universidad Politecnica de Madrid Espana</Affiliation><Affiliation>A Arquero Universidad Politecnica de Madrid Espana</Affiliation><Affiliation>I Molina Universidad Politecnica de Madrid Espana</Affiliation>")
