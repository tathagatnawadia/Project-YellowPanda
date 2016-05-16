# import nltk
# import re
# import sys
# import os
# from nltk.corpus import state_union
# from nltk.tokenize import PunktSentenceTokenizer
# rvalue=[]
# rkey=[]
# train_text=state_union.raw("2005-GWBush.txt")


# #Todo code

# def removeMultipleNewLines(str):
# 	newstr = re.sub('\n+', '\n', str)
# 	return newstr

# target_folder = os.path.join(os.getcwd(),'corpus','corrected')
# print(target_folder)
# print(" --------- Reading Corpus ------------")

# corpus = ""
# file_dumps = {}
# for i in os.listdir(target_folder):
# 	file_absolute_path = os.path.join(target_folder,i)
# 	if i == 'profit_loss.store': 
# 		corpus = removeMultipleNewLines(open(file_absolute_path, "r").read())

# list_of_questions = corpus.splitlines()
# print('Total number of questions are -> ',len(list_of_questions))
# #exit()

# #Todo code ends


# import spacy.en
# nlp = spacy.en.English()

# for question_text in list_of_questions:
# 	print("---------------------------")
# 	s = nlp(question_text)
# 	total_sentenses = list(s.sents)
# 	last_sentense = total_sentenses[-1]
# #	for sent in total_sentenses:
# #		print(sent)
	
# 	print(last_sentense)




'''
Vikas code to be integrated with Soundaryas
'''

import nltk
import re
import sys
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
rvalue=[]
rkey=[]
train_text=state_union.raw("2005-GWBush.txt")
# sample_text="A man can reach a certain place in 30 hours. The speed with which he travels is , If he reduces his speed by 1/15th, he goes 10 km less in that time."
# print(tokenized)
def process_content(text):
	print("\n---------------------------------------------------------------------------- \n")
	print(text)
	custom_sent_tokenizer=PunktSentenceTokenizer(train_text)
	tokenized=custom_sent_tokenizer.tokenize(text)
	try:
		for i in tokenized:
			words=nltk.word_tokenize(i)
			tagged=nltk.pos_tag(words)
			# print(tagged)
	except Exception as e:
		print(str(e))
	grammar = "NP: {<DT>?<JJ>*<NN>}"
	cp = nltk.RegexpParser(grammar)
	result = cp.parse(tagged)
	newset=result.leaves()
	noun = re.compile("NN")
	adverb= re.compile("RB")
	verb = re.compile("VBN")
	questionword=re.compile("WP")
	questionword2=re.compile("WRB")
	questionword3=re.compile("WDT")
	comma=re.compile(",")
	colon=re.compile(":")
	rvalue=[]
	rkey=[]
	for key,value in newset:
		rvalue.append(value)
		rkey.append(key)
	k=0
	z=0
	if z==0:
		for key,value in newset:
			k=k+1
			m=k
			if questionword.match(value) is not None:
				if z==1:
					break
				else:
					z=1
					for values in rvalue[k:]:
						if noun.match(values) is not None:
							print("objective is",rkey[m])
							break
						elif adverb.match(values) is not None:
							print("objective is ",rkey[m])
							break
						elif verb.match(values) is not None:
							print("objective is ",rkey[m])
							break
						m=m+1
			elif questionword2.match(value) is not None:
				if z==1:
					break
				else:
					z=1
					for values in rvalue[k:]:
						if noun.match(values) is not None:
							print("objective is",rkey[m])
							break
						elif adverb.match(values) is not None:
							print("objective is ",rkey[m])
							break
						elif verb.match(values) is not None:
							print("objective is ",rkey[m])
							break
						m=m+1
			elif questionword3.match(value) is not None:
				if z==1:
					break
				else:
					z=1
					for values in rvalue[k:]:
						if noun.match(values) is not None:
							print("objective is",rkey[m])
							break
						elif adverb.match(values) is not None:
							print("objective is ",rkey[m])
							break
						elif verb.match(values) is not None:
							print("objective is ",rkey[m])
							break
						m=m+1
			elif comma.match(value) is not None:
				if z==1:
					break
				else:
					z=1
					for values in rvalue[k:]:
						if noun.match(values) is not None:
							print("objective is",rkey[m])
							break
						elif adverb.match(values) is not None:
							print("objective is ",rkey[m])
							break
						elif verb.match(values) is not None:
							print("objective is ",rkey[m])
							break
						m=m+1
	if z==0:	
		for key,value in newset:
			if noun.match(value) is not None:
				print("objective is",key)
				break
			elif adverb.match(value) is not None:
				print("objective is ",key)
				break
			elif verb.match(value) is not None:
				print("objective is ",key)
				break

