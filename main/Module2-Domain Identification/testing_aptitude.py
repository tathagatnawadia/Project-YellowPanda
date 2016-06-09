from colorama import init
init()
from colorama import Fore, Back, Style
print(chr(27) + "[2J")
print(Fore.YELLOW + 'Loading the scripts ........... ')
print(Style.RESET_ALL)
import nltk
import random
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
import string

from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC

from nltk.classify import ClassifierI
from statistics import mode
import codecs
import os,re,operator

import spacy
nlp = spacy.en.English()

def checkVector(word):
	flag = 0
	w = nlp(word)
	for token in w:
		if token.is_stop == True or token.is_space == True or token.is_punct == True or token.like_num == True or len(str(token)) == 1:
			flag = 1
		if flag == 0:
			return True
		else:
			return False


def removeMultipleNewLines(str):
	newstr = re.sub('\n+', '\n', str)
	return newstr

import sys as Sys
# Print iterations progress
def printProgress (iteration, total, prefix = '', suffix = '', decimals = 2, barLength = 100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
    """
    filledLength    = int(round(barLength * iteration / float(total)))
    percents        = round(100.00 * (iteration / float(total)), decimals)
    bar             = '#' * filledLength + '-' * (barLength - filledLength)
    Sys.stdout.write('%s [%s] %s%s %s\r' % (prefix, bar, percents, '%', suffix)),
    Sys.stdout.flush()
    if iteration == total:
        print("\n")

corpus_folder = [os.path.join(os.getcwd(),'corpus','selected'),os.path.join(os.getcwd(),'corpus','notselected')]

file_dumps = {}
all_words = []
all_questions = []
domain_words = {}
universe_words = []

#Reading the corpus
c = 0
printProgress(c, len(corpus_folder), prefix = 'Loading Corpus into memory :', suffix = 'Complete', barLength = 50)
for folder in corpus_folder:
	c = c + 1
	printProgress(c, len(corpus_folder), prefix = 'Loading Corpus into memory :', suffix = 'Complete', barLength = 50)
	for i in os.listdir(folder):
		#For each domain file in the corpus open the file
		file_absolute_path = os.path.join(folder,i)
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

#Enhacing the feature vector (Remove punctutations, stop words, like numbers, spaces)

c = 0
printProgress(c, len(domain_words), prefix = 'Enhancing Machine Vector :', suffix = 'Complete', barLength = 50)
for domain in domain_words:
	c = c + 1
	printProgress(c, len(domain_words), prefix = 'Enhancing Machine Vector :', suffix = 'Complete', barLength = 50)
	new_word_list = []
	for word in domain_words[domain]:
		if checkVector(word) == True:
			new_word_list.append(word)
	domain_words[domain] = new_word_list


#Cleaning all_word list
universe_words = all_words
new_word_list = []
c = 0
printProgress(c, len(all_words), prefix = 'Cleaning Nullifiable Vector :', suffix = 'Complete', barLength = 50)
for word in all_words:
	c = c + 1
	printProgress(c, len(all_words), prefix = 'Cleaning Nullifiable Vector :', suffix = 'Complete', barLength = 50)
	if checkVector(word) == True:
		new_word_list.append(word)
all_words = new_word_list

for domain in file_dumps:
	for question in file_dumps[domain].splitlines():
		all_questions.append((question.strip(),domain))

print(Fore.YELLOW + 'SUMMARY')
print(Style.RESET_ALL)
random.shuffle(all_questions)

print("Length of corpus           : ",len(all_questions))
print("Total words in the corpus  : ",len(universe_words))
print("Unique words in the corpus : ",len(set(universe_words)))
print("Record shuffle status      :  Completed")
print("Total questions on record  : ",len(all_questions))



'''
Refining Machine Learning Technique for changing 
1.overall_limit
2.domain_limit

Finalising the feature vector

'''

overall_limit = 700
domain_limit = 25
learn_setting = 'OVERALL'














#Phase1: Overall Feature Vector
FD_relevant_words = nltk.FreqDist(all_words)
most_common_overall = FD_relevant_words.most_common(overall_limit)

#Phase2: Domainwise Feature Vector

FD_domain_words = {}
most_common_domainwise = []
for domain in domain_words:
	FD_domain_words[domain] = nltk.FreqDist(domain_words[domain])
for domain,FD in FD_domain_words.items():
	to_be_appended = FD.most_common(domain_limit)
	for value in to_be_appended:
		most_common_domainwise.append(value)

'''
print(most_common_overall)
print(most_common_domainwise)
'''
if learn_setting == 'DOMAIN':
	most_common = most_common_domainwise #Setting up with either (most_common_domainwise, most_common_overall)
else:
	most_common = most_common_overall

word_features = []
for common in most_common:
	word_features.append(common[0])
'''
print("FEATURE VECTOR :: ",word_features)
'''

def find_features(document):
	words = set(word_tokenize(document))
	features = {}
	for w in word_features:
		features[w] = (w in words)
	return features

featuresets = [(find_features(question), category) for (question,category) in all_questions] #(word_tokenized_review,sentiment) for 10000 movie reviews

random.shuffle(featuresets)
random.shuffle(featuresets)

training_set = featuresets[100:] #1900 reviews with (review,sentiment)
testing_set = featuresets[:100] #remaing revies with (review,sentiment)

print("Total size of the training data : ",len(training_set))
print("Total size of the testing  data : ",len(testing_set))


temp_result = []
classifier = nltk.NaiveBayesClassifier.train(training_set) #The classifier is ready with the training set
temp_result.append(nltk.classify.accuracy(classifier,testing_set)*100)
print("NLTK Original Naive Bayes Algo Accuracy : ",(nltk.classify.accuracy(classifier,testing_set))*100)
classifier.show_most_informative_features(15)

'''
Training 3 Naive Bayes Classifier and comparing the results

'''
MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
temp_result.append(nltk.classify.accuracy(MNB_classifier,testing_set)*100)
print("MNB_classifier Classifier : ",nltk.classify.accuracy(MNB_classifier,testing_set)*100)

	# GAU_classifier = SklearnClassifier(GaussianNB())
	# GAU_classifier.train(training_set)
	# print("GAU_classifier Classifier : ",nltk.classify.accuracy(GAU_classifier,testing_set)*100)

BER_classifier = SklearnClassifier(BernoulliNB())
BER_classifier.train(training_set)
temp_result.append(nltk.classify.accuracy(BER_classifier,testing_set)*100)
print("BER_classifier Classifier : ",nltk.classify.accuracy(BER_classifier,testing_set)*100)

'''
Training 2 Regression Based Classifier and comparing the results
'''

LogisticsRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticsRegression_classifier.train(training_set)
temp_result.append(nltk.classify.accuracy(LogisticsRegression_classifier,testing_set)*100)
print("LogisticsRegression_classifier Classifier : ",nltk.classify.accuracy(LogisticsRegression_classifier,testing_set)*100)

SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
SGDClassifier_classifier.train(training_set)
temp_result.append(nltk.classify.accuracy(SGDClassifier_classifier,testing_set)*100)
print("SGDClassifier_classifier Classifier : ",nltk.classify.accuracy(SGDClassifier_classifier,testing_set)*100)

'''
Training 3 Support Vector Machine Classifier and comparing the results
'''

SVC_classifier = SklearnClassifier(SVC())
SVC_classifier.train(training_set)
temp_result.append(nltk.classify.accuracy(SVC_classifier,testing_set)*100)
print("SVC_classifier Classifier : ",nltk.classify.accuracy(SVC_classifier,testing_set)*100)

LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
temp_result.append(nltk.classify.accuracy(LinearSVC_classifier,testing_set)*100)
print("LinearSVC_classifier Classifier : ",nltk.classify.accuracy(LinearSVC_classifier,testing_set)*100)

# NuSVC_classifier = SklearnClassifier(NuSVC())
# NuSVC_classifier.train(training_set)
# print("NuSVC_classifier Classifier : ",nltk.classify.accuracy(NuSVC_classifier,testing_set)*100)




class VoteClassifier(ClassifierI):
	def __init__(self, *classifiers):
		self._classifiers = classifiers

	def classify(self, features):
		votes = []
		for c in self._classifiers:
			v = c.classify(features)
			votes.append(v)
		return mode(votes)

	def confidence(self, features):
		votes = []
		for c in self._classifiers:
			v = c.classify(features)
			votes.append(v)

		choice_votes = votes.count(mode(votes))
		conf = choice_votes / len(votes)
		return conf
		
voted_classifier = VoteClassifier(classifier,
									MNB_classifier,
									BER_classifier,
									LogisticsRegression_classifier,
									SGDClassifier_classifier,
									SVC_classifier,
									LinearSVC_classifier)
print(voted_classifier)
									

print(Fore.YELLOW,'FIELD TESTING THE LEARNED MODEL ON THE TESTING DATA')
print(Style.RESET_ALL)

try:
	print("Classification:", len(testing_set[0][0])," ----- ",voted_classifier.classify(testing_set[0][0]), "Confidence %:",voted_classifier.confidence(testing_set[0][0])*100)
	print("Classification:", len(testing_set[1][0])," ----- ",voted_classifier.classify(testing_set[1][0]), "Confidence %:",voted_classifier.confidence(testing_set[1][0])*100)
	print("Classification:", len(testing_set[2][0])," ----- ",voted_classifier.classify(testing_set[2][0]), "Confidence %:",voted_classifier.confidence(testing_set[2][0])*100)
	print("Classification:", len(testing_set[3][0])," ----- ",voted_classifier.classify(testing_set[3][0]), "Confidence %:",voted_classifier.confidence(testing_set[3][0])*100)
	print("Classification:", len(testing_set[4][0])," ----- ",voted_classifier.classify(testing_set[4][0]), "Confidence %:",voted_classifier.confidence(testing_set[4][0])*100)
	#print("Classification:", len(testing_set[5][0])," ----- ",voted_classifier.classify(testing_set[5][0]), "Confidence %:",voted_classifier.confidence(testing_set[5][0])*100)
except Exception as e:
	print("The classifier had got a conflict !!")


while True:
	try:
		print(" ########################### ")
		terminal_text = input('Question : ')
		if terminal_text == 'exit':
			break
		terminal_text_feature = find_features(terminal_text) #(word_tokenized_review,sentiment) for 10000 movie reviews

		print(Fore.RED,'\nResults')	
		print(Style.RESET_ALL)
		print("Classification:", len(terminal_text_feature)," ----- ",voted_classifier.classify(terminal_text_feature), "Confidence %:",voted_classifier.confidence(terminal_text_feature)*100)
	except Exception as e:
		print(Fore.RED,'\nResults')	
		print(Style.RESET_ALL)
		print("Unable to classify.")