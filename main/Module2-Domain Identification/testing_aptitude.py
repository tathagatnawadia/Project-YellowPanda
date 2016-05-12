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
punct = set(string.punctuation)
english_stops = set(stopwords.words('english'))

def removeMultipleNewLines(str):
	newstr = re.sub('\n+', '\n', str)
	return newstr

target_folder = os.path.join(os.getcwd(),'corpus','indiabix')

file_dumps = {}
all_words = []
all_questions = []
domain_words = {}





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

print(" ---- 20 most common words for each domain ----")
FD_domain_words = {}
for domain in domain_words:
	FD_domain_words[domain] = nltk.FreqDist(domain_words[domain])
	print("For domain --> ",domain)
	print(FD_domain_words[domain].most_common(20))
	print("-------------------")
'''
Legend
all_words contain all the words in the corpus (We will analyse these words and get a Frequency Distribution from all these
'''

'''
foreach domain
all_question = [(Question1,'Profit Loss'), (Question2,'HCF LCM'), (Question1,'Trains'), (Question1,'Profit Loss') .......... ]
'''
for domain in file_dumps:
	for question in file_dumps[domain].split('\n'):
		all_questions.append((question.strip(),domain))

random.shuffle(all_questions)

seepage = ['The','the','a','A','What']
unique_words = set(all_words)
relevant_words_punctuation = [word for word in all_words if word not in english_stops and not word.isdigit() and word not in seepage]
relevant_words = [word for word in relevant_words_punctuation if word not in punct]

FD_all_words = nltk.FreqDist(all_words)
FD_relevant_words = nltk.FreqDist(relevant_words)

'''
Generating some reports based on the corpus
'''
print("Length of corpus           : ",len(all_questions))
print("Total words in the corpus  : ",len(all_words))
print("Total relevant words in corpus (excluding StopWords) : ",len(relevant_words))
print("Unique words in the corpus : ",len(unique_words))


##################################################################
#Apply the Naive Based Classifier

word_features = []
most_commons = FD_relevant_words.most_common(50)
for common in most_commons:
	word_features.append(common[0])
	
print("Feature Vector : ",word_features)

def find_features(document):
	words = set(word_tokenize(document))
	features = {}
	for w in word_features:
		features[w] = (w in words)
	return features

featuresets = [(find_features(question), category) for (question,category) in all_questions] #(word_tokenized_review,sentiment) for 10000 movie reviews

random.shuffle(featuresets)

training_set = featuresets[:50] #1900 reviews with (review,sentiment)
testing_set = featuresets[50:] #remaing revies with (review,sentiment)

print("Total size of the data : ",len(featuresets))
print("Total size of the training data : ",len(training_set))
print("Total size of the testing  data : ",len(testing_set))



classifier = nltk.NaiveBayesClassifier.train(training_set) #The classifier is ready with the training set

print("NLTK Original Naive Bayes Algo Accuracy : ",(nltk.classify.accuracy(classifier,testing_set))*100)
classifier.show_most_informative_features(15)

'''

Training 3 Naive Bayes Classifier and comparing the results

'''
MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MNB_classifier Classifier : ",nltk.classify.accuracy(MNB_classifier,testing_set)*100)

#GAU_classifier = SklearnClassifier(GaussianNB())
#GAU_classifier.train(training_set)
#print("GAU_classifier Classifier : ",nltk.classify.accuracy(GAU_classifier,testing_set)*100)

BER_classifier = SklearnClassifier(BernoulliNB())
BER_classifier.train(training_set)
print("BER_classifier Classifier : ",nltk.classify.accuracy(BER_classifier,testing_set)*100)

'''

Training 2 Regression Based Classifier and comparing the results

'''

LogisticsRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticsRegression_classifier.train(training_set)
print("LogisticsRegression_classifier Classifier : ",nltk.classify.accuracy(LogisticsRegression_classifier,testing_set)*100)

SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
SGDClassifier_classifier.train(training_set)
print("SGDClassifier_classifier Classifier : ",nltk.classify.accuracy(SGDClassifier_classifier,testing_set)*100)

'''

Training 3 Support Vector Machine Classifier and comparing the results

'''

SVC_classifier = SklearnClassifier(SVC())
SVC_classifier.train(training_set)
print("SVC_classifier Classifier : ",nltk.classify.accuracy(SVC_classifier,testing_set)*100)

LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print("LinearSVC_classifier Classifier : ",nltk.classify.accuracy(LinearSVC_classifier,testing_set)*100)

NuSVC_classifier = SklearnClassifier(NuSVC())
NuSVC_classifier.train(training_set)
print("NuSVC_classifier Classifier : ",nltk.classify.accuracy(NuSVC_classifier,testing_set)*100)



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
									LinearSVC_classifier,
									NuSVC_classifier)
									
								
print("Classification:", len(testing_set[0][0])," ----- ",voted_classifier.classify(testing_set[0][0]), "Confidence %:",voted_classifier.confidence(testing_set[0][0])*100)
print("Classification:", len(testing_set[1][0])," ----- ",voted_classifier.classify(testing_set[1][0]), "Confidence %:",voted_classifier.confidence(testing_set[1][0])*100)
print("Classification:", len(testing_set[2][0])," ----- ",voted_classifier.classify(testing_set[2][0]), "Confidence %:",voted_classifier.confidence(testing_set[2][0])*100)
print("Classification:", len(testing_set[3][0])," ----- ",voted_classifier.classify(testing_set[3][0]), "Confidence %:",voted_classifier.confidence(testing_set[3][0])*100)
print("Classification:", len(testing_set[4][0])," ----- ",voted_classifier.classify(testing_set[4][0]), "Confidence %:",voted_classifier.confidence(testing_set[4][0])*100)
print("Classification:", len(testing_set[5][0])," ----- ",voted_classifier.classify(testing_set[5][0]), "Confidence %:",voted_classifier.confidence(testing_set[5][0])*100)

		