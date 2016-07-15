# -*- coding: utf-8 -*-
from django.db import models

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/')

class UserDetails(models.Model):
	"""docstring for rPapers"""
	paperid = models.FloatField()
	userid = models.CharField(max_length= 100)
	user_email = models.EmailField()
	def __str__(self):
		return self.paperid

class Response(models.Model):
	"""docstring for response"""
	# userdetails = models.ForeignKey(UserDetails)
	# paperid = models.IntegerField()
	user_email = models.EmailField()
	title = models.FloatField()
	authorNames = models.FloatField()
	urls = models.FloatField()
	email = models.FloatField()
	affiliation = models.FloatField()
	# references = models.FloatField()
	sections = models.FloatField()
	emailAuthMap = models.FloatField()
	figHeading = models.FloatField()
	Footnotes = models.FloatField()
	TableHeading = models.FloatField()
	# citToRef = models.FloatField()

	def __str__(self):
		return self.title
