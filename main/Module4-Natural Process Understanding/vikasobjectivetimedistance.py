import nltk
import re
import os
import sys
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

for sample_text in list_of_questions:
	print('--------------------------------------------------------------------------------------------------------------------------------------------------')
	sample_text = 'What is the population of india? Note that we arent considering the demographics of 2016'
	words=sample_text.split()
	print(words)
	custom_sent_tokenizer=PunktSentenceTokenizer(train_text)
	tokenized=custom_sent_tokenizer.tokenize(sample_text)
	# print(tokenized)
	def process_content():
		try:
			for i in tokenized:
				words=nltk.word_tokenize(i)
				tagged=nltk.pos_tag(words)
				# print(tagged)
		except Exception as e:
			print(str(e))
		print("objective sentence",tagged)
		grammar = "NP: {<DT>?<JJ>*<NN>}"
		cp = nltk.RegexpParser(grammar)
		result = cp.parse(tagged)
		newset=result.leaves()
		noun = re.compile("NN")
		adverb= re.compile("RB")
		verb = re.compile("VBN")
		questionword=re.compile("WP")
		questionword2=re.compile("WRB")
		comma=re.compile(",")
		for key,value in newset:
			rvalue.append(value)
			rkey.append(key)
		k=0
		for key,value in newset:
			k=k+1
			m=k
			if questionword.match(value) is not None:
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
				#result.draw()
			elif questionword2.match(value) is not None:
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
				#result.draw()
			elif comma.match(value) is not None:
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
				#result.draw()
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
		#result.draw()
	process_content()
	sys.exit(0)
