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

def removeMultipleNewLines(str):
	newstr = re.sub('\n+', '\n', str)
	return newstr

target_folder = os.path.join(os.getcwd(),'corpus','indiabix')

file_dumps = {}
all_words = []
all_questions = []
domain_words = {}
question_collection = []




for i in os.listdir(target_folder):
	#For each domain file in the corpus open the file
	file_absolute_path = os.path.join(os.getcwd(),'corpus','indiabix',i)
	#If the file is a .store file open and read the file
	if i.endswith(".store"): 
		'''
		file_dumps['Profit and Loss'] = "Question1\nQuestion2" and so on
		'''
		file_dumps[i] = removeMultipleNewLines(open(file_absolute_path, "r").read())
		#For each word in the domain, add it to the all_words list
		temp = []
		for word in word_tokenize(file_dumps[i]):
			all_words.append(word)
			temp.append(word)
		'''
		domain_words will take in all the words used in a domain
		domain_words['HCF LCM']=['The','and','The','a' .......] 
		'''	
		domain_words[i] = temp
		for s in file_dumps[i].splitlines():
			question_collection.append((s,i))


print("++++++++++++++++++++++++++++++++++++++++++++++")
#for random_question in question_collection:
#	print(random_question[0])
#	print("-----")

tokensPerQuestion = [nltk.word_tokenize(random_question[0]) for random_question in question_collection]
tokensPerQuestion = [[token.lower() for token in t if token.lower() not in symbols and token.lower() not in stoplist] for t in tokensPerQuestion]
print(tokensPerQuestion[:5])

b = list(chain(*[(list(bigrams(tokens))) for tokens in tokensPerQuestion]))
t = list(chain(*[(list(trigrams(tokens))) for tokens in tokensPerQuestion]))

print(b)
fdist = nltk.FreqDist(b)
plt.figure(figsize=(20, 8))
# plot the top 20 bigrams
fdist.plot(30)

fdist = nltk.FreqDist(t)
plt.figure(figsize=(20, 8))
# plot the top 20 trigrams
fdist.plot(30)

		