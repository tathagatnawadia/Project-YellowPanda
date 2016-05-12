'''
The aims for this module is to 

Phase 1

1. Read the cleaned corpus from ./corpus/corrected
2. Find the last sentense from each question.
3. If the last question has { , ; : } in the middle then we treat the last delimited as the objective question and the rest as given
4. Find all the NOUNS, PREPOSITIONS, ADJECTIVES, NUMERICAL DATA in the objective phrase

Phase 2

1.Treat the non objective of the question as GIVEN(although GIVEN can also be hidden in the objective phrase)
2.Find all the NOUNS, PREPOSITIONS, ADJECTIVES, NUMERICAL DATA in the GIVEN

Phase 3

1.Get the properties of the domain by top repeating words (Eg. 

Todo : Embedding of a word by using word2vec

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

target_folder = os.getcwd()
#print(target_folder)

file_dumps = {}
all_words = []
all_questions = []
domain_words = {}
question_collection = []




for i in os.listdir(target_folder):
	#For each domain file in the corpus open the file
	file_absolute_path = os.path.join(os.getcwd(),i)
	#If the file is a .store file open and read the file
	if i.endswith(".store"): 
		'''
		file_dumps['Profit and Loss'] = "Question1\nQuestion2" and so on
		'''
		file_dumps[i] = removeMultipleNewLines(open(file_absolute_path, "r").read())
		#print(file_dumps[i])

domain_question_list = {}
for domain,domain_file_dump in file_dumps.items():
	domain_question_list[domain] = domain_file_dump.splitlines()
	print("Domain -> ",domain," has ",len(domain_question_list[domain])," questions")

'''
Double For Loop
1st For Loop - Iterating on the domains
2nd For Loop - Iterating on the question list of the domain
'''
for domain,questions in domain_question_list.items():
	for question in questions[-1:]:
		sentense = {}
		sentense_roots = []
		q = nlp(question.replace("Rs.","Rs"))
		print(q)
		sentense['Total Sentenses'] = len(list(q.sents))
#		sentense['Noun Chunks'] = 
#		sentense['Entities'] = 
		print("Total Sentenses --> ",len(list(q.sents)))
		print("Noun Chunks --> ",list(q.noun_chunks))
		print("Entities    --> ",list(q.ents))
		print("GENERATING SENTENSE ROOTS")

		for s in q.sents:
			sentense_roots.append(s)
		
		print(sentense_roots)
		print("GENERATING NOUN CHUNK")
		
		noun_chunks = []
		for chunk in list(q.noun_chunks):
			noun = {}
			noun['chunk'] = chunk.orth_
			noun['primary_root'] = chunk.root.head.orth_
			noun['secondary_root'] = chunk.root
			noun_chunks.append(noun)
		sentense['noun_chunks'] = noun_chunks
		print("GENERATING THE SENTENSE DATA STRUCTURE")

		stats = []
		index = 0
		for token in q:
			token_property = {}
			token_property['token_position'] = index
			index = index + 1
			token_property['if_title'] = token.is_title
			token_property['if_punct'] = token.is_punct
			token_property['if_oov'] = token.is_oov
			token_property['if_stop'] = token.is_stop
			token_property['log_prob'] = token.prob
			token_property['token_index'] = token.idx
			token_property['token_legend'] = token.pos_
			token_property['token_deeplegend'] = token.tag_
			token_property['token_head'] = token.head
			stats.append((token,token_property))
		
		sentense['Original'] = stats
#		for token in sentense['Original']:
#			print(token)
#			print("---------")


#Starting the proximity sensing algo
	
''' 
We start by tokenising the entire sentense,
(WORD,POSITION,POS,TAG,ROOT_LEVEL,HEAD,SENTENSE)
'''
import collections


class oscillator:
	sent_oscillator = collections.namedtuple('Oscillator',['right_flag','right_pivot','right_deadend','left_flag','left_pivot','left_deadend','point','universe'])
	
def oscillator(point,universe):
	osc =  
	hop_count = 1
	while hop_count < universe:
		if right_flag == 1 and right_deadend == 0:
			right_flag = 0
			left_flag = 1
			right_pivot += 1
			right_deadend = comparator(right_pivot, universe)
			hop_count += 1
			print(right_pivot)
		elif left_flag == 1 and left_deadend == 0:
			left_flag = 0
			right_flag = 1
			left_pivot -= 1
			left_deadend = comparator(left_pivot, universe)
			hop_count += 1
			print(left_pivot)
	return point-1
		
def comparator(pivot,universe):
	if pivot < 0:
		return 1
	elif pivot > universe:
		return 1
	else:
		return 0

def reverse(a):
	if a == 1:
		return -1
	else:
		return 1

total = 40
pivot = 13
print(oscillator(pivot, total))
		
		
