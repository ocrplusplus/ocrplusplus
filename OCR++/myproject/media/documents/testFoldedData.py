import os
import glob
import subprocess
from subprocess import Popen, PIPE
import unicodedata

directory = "/var/www/html/OCR++/myproject/media/documents/"


def testFoldedData():
	file_name = glob.glob(directory+'testFiles/*.txt')[0]
	fn = file_name.split('/')
	fn = fn[-1]
	
	model = "cora_train_model.txt"
	# print "modelFile = " + model
	test_file = directory + "testFiles/"+fn
	test_fileR = directory + "testResults/"+fn
	subprocess.call("crf_test -m "+ model +" "+ test_file + " > "+ test_fileR, shell=True)
