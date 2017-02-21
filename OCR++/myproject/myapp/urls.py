# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('myproject.myapp.views',
    url(r'^$', 'home', name = 'home')
    url(r'^list/$', 'list', name='list'),
    url(r'^list/runScript/$', 'runScript', name='runScript'),
    # url(r'^list/vote/$', 'vote', name='vote'),
    # url(r'^list/upload/$', 'upload', name='upload'),
)
