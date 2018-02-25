# -*- coding: utf-8 -*-
from __future__ import division
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import glob
from myproject.myapp.models import Document
from myproject.myapp.models import Response, UserDetails
from myproject.myapp.forms import DocumentForm
import subprocess
from subprocess import Popen, PIPE
import os.path
import threading

script_dir = "/var/www/html/OCR++/myproject/myapp/"
directory = "/var/www/html/OCR++/myproject/media/documents/"
lock = threading.Lock()

def runScript(request):
    # print "ayaya"
    subprocess.call("rm " + directory + "input.pdf", shell=True)
    subprocess.call(directory + "Clean.sh",shell=True)
    # print "runn"
    # print paperid
    file_name = glob.glob(directory+'*.pdf')
    # print file_name
    srno = 1
    fname = file_name[0]
    fn = fname.split('/')
    fn = fn[-1]
    # print "Views.py : "+fn
    # subprocess.call("clear", shell=True)
    subprocess.call("rm -r " + directory + "eval_*.txt", shell=True)
    subprocess.call("rm -r " + directory + "*op.txt", shell=True)
    subprocess.call("rm " + directory + "Secmap.xml", shell=True)
    subprocess.call("rm -r " + directory + "TitleAuthor.xml", shell=True)
    subprocess.call("rm -r " + directory + "input*", shell=True)
    subprocess.call("rm -r " + directory + "final*", shell=True)

    subprocess.call("mv " + directory + fn + " " + directory + "input.pdf", shell=True)
    # subprocess.call("rm -r /var/www/html/media/documents/*",shell=True)
    subprocess.call("mkdir " + directory + "sessions/" + request.session['id'],shell=True)
    
    subprocess.call("mkdir /var/www/html/media/documents/sessions/" + request.session['id'],shell=True)
    subprocess.call("cp " + directory + "input.pdf /var/www/html/media/documents/sessions/" + request.session['id'] + "/", shell=True)
    subprocess.call("cp -r " + directory + "paper/* /var/www/html/media/documents/", shell=True)

    # subprocess.call("cp -r " + directory + "eval* /var/www/html/media/documents/",shell=True)
    # subprocess.call("cp -r " + directory + "sessions/blank " + directory + "sessions/" + request.session['id'],shell=True)

    # subprocess.call("python " + directory + "main_script_batch.py", shell=True)
    subprocess.call(directory + "ShellScript.sh",shell=True)
    
    subprocess.call("cp -r " + directory + "output.xml /var/www/html/media/documents/sessions/" + request.session['id'] + "/",shell=True)
    subprocess.call("cp -r " + directory + "output.xml " + directory + "sessions/" + request.session['id'] + "/",shell=True)
    subprocess.call("cp -r " + directory + "input.xml /var/www/html/media/documents/sessions/" + request.session['id'] + "/",shell=True)
    subprocess.call("cp -r " + directory + "input.xml " + directory + "sessions/" + request.session['id'] + "/",shell=True)
    subprocess.call("cp -r " + directory + "eval_* " + directory + "sessions/" + request.session['id'] + "/",shell=True)
    subprocess.call("cp -r " + directory + "input.pdf " + directory + "sessions/" + request.session['id'] + "/",shell=True)

    return HttpResponse("Done")

def list(request):
    if request.method == 'GET':
        return HttpResponseRedirect("/home/")
        # return HttpResponse('This page shows a list of most recent posts.')
        # pass
    # Handle file upload
    if request.method == 'POST':

        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            # Manage Sessions
            lock.acquire()
            sId = '0'
            try:
                sId = open("sessionId.txt",'rb').read()
            except Exception as e:
                print e
            try:
                sId = str((int(sId))+1)
            except Exception as e:
                sId = '1'
                print e
            open("sessionId.txt",'wb').write(sId)
            request.session['id'] = sId
            # lock.release()

            newdoc = Document(docfile = request.FILES['docfile'])
            fname = request.FILES['docfile'].name
            request.session['filename'] = fname
            newdoc.save()
            runScript(request)
            lock.release()

            # Redirect to the document list after POST
            return HttpResponseRedirect("../home/")
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'home.html',
        {'documents': documents, 'form': form},

        context_instance=RequestContext(request)
    )

def author_names(request):
    if request.session.has_key('id'):
        print "Session ID: ", request.session['id']
    else:
        request.session['id'] = '0'
        print "No session"
    return render(request, "author_names.html", {"session_id" : request.session['id']})

def title(request):
    if request.session.has_key('id'):
        print "Session ID: ", request.session['id']
    else:
        request.session['id'] = '0'
        print "No session"
    return render(request, "title.html", {"session_id" : request.session['id']})

def home(request):
    if request.session.has_key('id'):
        print "Session ID: ", request.session['id']
    else:
        request.session['id'] = '0'
        print "No session"
    return render(request, "home.html", {"session_id" : request.session['id']})

def email(request):
    if request.session.has_key('id'):
        print "Session ID: ", request.session['id']
    else:
        request.session['id'] = '0'
        print "No session"
    return render(request, "email.html", {"session_id" : request.session['id']})

def affiliation(request):
    if request.session.has_key('id'):
        print "Session ID: ", request.session['id']
    else:
        request.session['id'] = '0'
        print "No session"
    return render(request, "affiliation.html", {"session_id" : request.session['id']})

def map(request):
    if request.session.has_key('id'):
        print "Session ID: ", request.session['id']
    else:
        request.session['id'] = '0'
        print "No session"
    return render(request, "map.html", {"session_id" : request.session['id']})

def section(request):
    if request.session.has_key('id'):
        print "Session ID: ", request.session['id']
    else:
        request.session['id'] = '0'
        print "No session"
    return render(request, "section.html", {"session_id" : request.session['id']})

def table_heading(request):
    if request.session.has_key('id'):
        print "Session ID: ", request.session['id']
    else:
        request.session['id'] = '0'
        print "No session"
    return render(request, "table_heading.html", {"session_id" : request.session['id']})

def figure_heading(request):
    if request.session.has_key('id'):
        print "Session ID: ", request.session['id']
    else:
        request.session['id'] = '0'
        print "No session"
    return render(request, "figure_heading.html", {"session_id" : request.session['id']})

def url(request):
    if request.session.has_key('id'):
        print "Session ID: ", request.session['id']
    else:
        request.session['id'] = '0'
        print "No session"
    return render(request, "url.html", {"session_id" : request.session['id']})

def footnote(request):
    if request.session.has_key('id'):
        print "Session ID: ", request.session['id']
    else:
        request.session['id'] = '0'
        print "No session"
    return render(request, "footnote.html", {"session_id" : request.session['id']})

def citref(request):
    if request.session.has_key('id'):
        print "Session ID: ", request.session['id']
    else:
        request.session['id'] = '0'
        print "No session"
    return render(request, "citref.html", {"session_id" : request.session['id']})

def ref_feature(request):
    if request.session.has_key('id'):
        print "Session ID: ", request.session['id']
    else:
        request.session['id'] = '0'
        print "No session"
    return render(request, "reference.html", {"session_id" : request.session['id']})

def team(request):
    return render(request, "team.html")

def getauthor(request):
    if request.method == 'GET':
        resp = ""
        # print directory + "sessions/" + request.session['id'] + "/" + "eval_author.txt"
        if os.path.isfile(directory + "sessions/" + request.session['id'] + "/" + "eval_author.txt"):
            resp = open(directory + "sessions/" + request.session['id'] + "/" + "eval_author.txt").read()
            if len(resp)==0:
                resp = "No file"
        else:
            resp = "No file"

        response = {'status': 1, 'message': "Confirmed!!", 'url':'/author_names/'}
        return HttpResponse(resp, content_type='string')

def gettitle(request):
    if request.method == 'GET':
        resp = ""
        if os.path.isfile(directory + "sessions/" + request.session['id'] + "/" + "eval_title.txt"):
            resp = open(directory + "sessions/" + request.session['id'] + "/" + "eval_title.txt").read()
            if len(resp)==0:
                resp = "No file"
        else:
            resp = "No file"

        response = {'status': 1, 'message': "Confirmed!!", 'url':'/title/'}
        return HttpResponse(resp, content_type='string')

def getemail(request):
    if request.method == 'GET':
        resp = ""
        if os.path.isfile(directory + "sessions/" + request.session['id'] + "/" + "eval_emails.txt"):
            resp = open(directory + "sessions/" + request.session['id'] + "/" + "eval_emails.txt").read()
            if len(resp)==0:
                resp = "No file"
        else:
            resp = "No file"

        response = {'status': 1, 'message': "Confirmed!!", 'url':'/email/'}
        return HttpResponse(resp, content_type='string')

def getaffiliation(request):
    if request.method == 'GET':
        resp = ""
        if os.path.isfile(directory + "sessions/" + request.session['id'] + "/" + "eval_Affiliations.txt"):
            resp = open(directory + "sessions/" + request.session['id'] + "/" + "eval_Affiliations.txt").read()
            if len(resp)==0:
                resp = "No file"
        else:
            resp = "No file"

        response = {'status': 1, 'message': "Confirmed!!", 'url':'/affiliation/'}
        return HttpResponse(resp, content_type='string')

def getmap(request):
    if request.method == 'GET':
        resp = ""
        if os.path.isfile(directory + "sessions/" + request.session['id'] + "/" + "eval_map.txt"):
            resp = open(directory + "sessions/" + request.session['id'] + "/" + "eval_map.txt").read()
            if len(resp)==0:
                resp = "No file"
        else:
            resp = "No file"

        response = {'status': 1, 'message': "Confirmed!!", 'url':'/map/'}
        return HttpResponse(resp, content_type='string')

def getsection(request):
    if request.method == 'GET':
        resp = ""
        if os.path.isfile(directory + "sessions/" + request.session['id'] + "/" + "eval_Secmap.txt"):
            resp = open(directory + "sessions/" + request.session['id'] + "/" + "eval_Secmap.txt").read()
            if len(resp)==0:
                resp = "No file"
        else:
            resp = "No file"

        response = {'status': 1, 'message': "Confirmed!!", 'url':'/section/'}
        return HttpResponse(resp, content_type='string')

def gettabfig(request):
    if request.method == 'GET':
        resp = ""
        if os.path.isfile(directory + "sessions/" + request.session['id'] + "/" + "eval_tables_figures.txt"):
            resp = open(directory + "sessions/" + request.session['id'] + "/" + "eval_tables_figures.txt").read()
            if len(resp)==0:
                resp = "No file"
        else:
            resp = "No file"

        response = {'status': 1, 'message': "Confirmed!!", 'url':'/table_heading/'}
        return HttpResponse(resp, content_type='string')

def geturl(request):
    if request.method == 'GET':
        resp = ""
        if os.path.isfile(directory + "sessions/" + request.session['id'] + "/" + "eval_url.txt"):
            resp = open(directory + "sessions/" + request.session['id'] + "/" + "eval_url.txt").read()
            if len(resp)==0:
                resp = "No file"
        else:
            resp = "No file"

        response = {'status': 1, 'message': "Confirmed!!", 'url':'/url/'}
        return HttpResponse(resp, content_type='string')

def getfootnote(request):
    if request.method == 'GET':
        resp = ""
        if os.path.isfile(directory + "sessions/" + request.session['id'] + "/" + "eval_footnote.txt"):
            resp = open(directory + "sessions/" + request.session['id'] + "/" + "eval_footnote.txt").read()
            if len(resp)==0:
                resp = "No file"
        else:
            resp = "No file"

        response = {'status': 1, 'message': "Confirmed!!", 'url':'/footnote/'}
        return HttpResponse(resp, content_type='string')

def getcitref(request):
    if request.method == 'GET':
        resp = ""
        # print os.path.isfile(directory + "eval_cit2ref.xml")
        if os.path.isfile(directory + "sessions/" + request.session['id'] + "/" + "eval_cit2ref.txt"):
            # print "aya toh****************"
            resp = open(directory + "sessions/" + request.session['id'] + "/" + "eval_cit2ref.txt").read()
            if len(resp)==0:
                resp = "No file"
        else:
            resp = "No file"

        response = {'status': 1, 'message': "Confirmed!!", 'url':'/citref/'}
        return HttpResponse(resp, content_type='string')

def getref_feature(request):
    # if request.method == 'GET':
    #     resp = ""
    #     if os.path.isfile(directory + "testResults/xmls/input.xml"):
    #         resp = open(directory + "testResults/xmls/input.xml").read()
    #         if len(resp)==0:
    #             resp = "No file"
    #     else:
    #         resp = "No file"

    #     response = {'status': 1, 'message': "Confirmed!!", 'url':'/ref_feature/'}
    #     return HttpResponse(resp, content_type='string')
    if request.method == 'GET':
        resp = ""
        if os.path.isfile(directory + "sessions/" + request.session['id'] + "/" + "eval_ref.txt"):
            # print "aya toh****************"
            resp = open(directory + "sessions/" + request.session['id'] + "/" + "eval_ref.txt").read()
            if len(resp)==0:
                resp = "No file"
        else:
            resp = "No file"

        response = {'status': 1, 'message': "Confirmed!!", 'url':'/ref_feature/'}
        return HttpResponse(resp, content_type='string')
