'''
Phase 1:

1.Extract what kind of units are being used in a domain. {'domain':[unit1,unit2,unit3,unit4]}

Phase 2:
	
1.Extract features of a domain using singleton,bigrams,trigrams analysis {'domain':['Feature1','Feature2','Feature3','Feature4']}

'''

import nltk
import random
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.util import bigrams, trigrams
from itertools import chain
import matplotlib.pyplot as plt
import numpy as np

import string

from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC

from nltk.classify import ClassifierI
from statistics import mode
import codecs
import os,re,operator
symbols = set(string.punctuation)
stoplist = set(stopwords.words('english'))

import spacy.en
nlp = spacy.en.English()

def removeMultipleNewLines(str):
	newstr = re.sub('\n+', '\n', str)
	return newstr

target_folder = os.path.join(os.getcwd(),'corpus','corrected')
print(target_folder)
print(" --------- Reading Corpus ------------")
corpus = ""
file_dumps = {}
for i in os.listdir(target_folder):
	file_absolute_path = os.path.join(target_folder,i)
	if i.endswith(".store"): 
		'''
		file_dumps['Profit and Loss'] = "Question1\nQuestion2" and so on
		'''
		file_dumps[i] = removeMultipleNewLines(open(file_absolute_path, "r").read())


for domain,text in file_dumps.items():
	file_dumps[domain] = text.splitlines()
	print('DOMAIN :: ',domain,' -> ',len(file_dumps[domain]), ' QUESTIONS')
	
'''
Do a unit analyiss
'''

unit_analysis = {}
for domain,questions in file_dumps.items():
	units = []
	units_pos = []
	print("----------------------------------",domain,"----------------------------------")
	for question in questions:
		temp_spacy = nlp(question)
		for token in temp_spacy:
			if token.pos_ == 'NUM':
				s = token.head
				units.append(str(s))
				units_pos.append(str(s.pos_))
				migrate = token.head
				if temp_zygote.pos_ == 'NOUN':
					units.append(str(token.head))
	unique_units = list(set(units))
	FD_units = nltk.FreqDist(units)
	FD_units_pos = nltk.FreqDist(units_pos)
	#print(FD_units.most_common(20))
	#print(FD_units_pos.most_common(20))

for domain,questions in file_dumps.items():
	for question in questions[-2:]:
		objects_relation = []
		#Adding Natural Spice
		temp_question = nlp(question)
		for token in temp_question:
			
		
				


print(" --------- Making a seperate correction folder ---------- ")

newdirectory = os.path.join(os.getcwd(),'corpus','metadata')
if not os.path.exists(newdirectory):
	os.makedirs(newdirectory)
else:
	print("Folder Already Exists, Truncating Folder ......... ")
	for dirfile in os.listdir(newdirectory): 
		file_path = os.path.join(newdirectory, dirfile)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
		except Exception as e:
			print(e)




			

