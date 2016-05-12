import nltk
import re
import sys
import os
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
rvalue=[]
rkey=[]
train_text=state_union.raw("2005-GWBush.txt")


#Todo code

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
	if i == 'profit_loss.store': 
		corpus = removeMultipleNewLines(open(file_absolute_path, "r").read())

list_of_questions = corpus.splitlines()
print('Total number of questions are -> ',len(list_of_questions))
#exit()

#Todo code ends


import spacy.en
nlp = spacy.en.English()

for question_text in list_of_questions:
	print("---------------------------")
	s = nlp(question_text)
	total_sentenses = list(s.sents)
	last_sentense = total_sentenses[-1]
#	for sent in total_sentenses:
#		print(sent)
	
	print(last_sentense)