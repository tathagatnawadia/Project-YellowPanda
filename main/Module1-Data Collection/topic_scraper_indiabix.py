from pymongo import MongoClient
from bs4 import BeautifulSoup
import urllib.request
import os.path
from json import *
'''
Function : Slices Dictionary (n)
'''
def slicedict(d, s):
	return {k:v for k,v in d.items() if k.startswith(s)}
'''
Establishing a mongo connection for storing the entire collection into MongoDB for faster retrieval of URLs
'''

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.indiabix

urlCollection = db.urlCollection

'''
Root of all Domains
'''
r = urllib.request.urlopen('http://www.indiabix.com/aptitude/questions-and-answers/').read()
prefix = "http://www.indiabix.com"
soup = BeautifulSoup(r,"lxml")
nohtml = soup.get_text()

'''
Getting all Domain Links
'''
aptitude_topics = str(soup.findAll("table", { "id" : "ib-tbl-topics" }))
a = BeautifulSoup(aptitude_topics,"lxml")

'''
Iterating over each of the link and store topic_store = { DOMAIN_NAME : DOMAIN_QUESTION_URL }
'''
topic_store = {}
for link in a.find_all('a'):
	url = prefix+link.get('href')
	topic = link.get_text();
	topic_store[topic] = url

'''
Getting all pages of each Domain futhur_links = { DOMAIN NAME : [ Page1, Page2, Page3 ] }
'''

furthur_links = {}
for key,value in topic_store.items():
	print("Fetching for " + value)
	temp = urllib.request.urlopen(str(value)).read()
	soup = BeautifulSoup(temp,"lxml")
	furthur_links[key] = []
	furthur_links[key].append(value)
	next_links = (soup.findAll("p", { "class" : "ib-pager" }))[0].find_all('a')
	for link in next_links:
		href = prefix+link.get('href')
		furthur_links[key].append(href)
'''
furthur_links will have all the pages for each recognized domain
{'Calendar': ['http://www.indiabix.com/aptitude/calendar/', 'http://www.indiabix.com/aptitude/calendar/062002', 'http://www.indiabix.com/aptitude/calendar/062003', 'http://www.indiabix.com/aptitude/calendar/062002'], ........... }

'''
for domain in furthur_links:
	#Opening a file for each domain
	domain_file_name = "corpus/indiabix/"+domain+".store"
	if os.path.isfile(domain_file_name):
		print("Skipping : ",domain)
		continue
	domain_file = open(domain_file_name, 'w')
	print("Creating Files for ",domain)
	for domain_page_link in furthur_links[domain]:
		r = urllib.request.urlopen(domain_page_link).read()
		soup = BeautifulSoup(r,"lxml")
		questions_div = soup.findAll("div", { "class" : "bix-div-container" })
		for question_div in questions_div:
			objective = {}
			i = 1
			question = (question_div.findAll("td",{ "class" : "bix-td-qtxt" } ))[0].get_text().strip().replace('\n', ' ').replace('\r', '').replace('  ',' ')
			options = (question_div.findAll("table", { "class" : "bix-tbl-options" }))[0].findAll("td", {"class" : "bix-td-option", "width" : "49%"})
			for option in options:
				objective[i] = option.get_text().strip().replace('\n', ' ').replace('\r', '').replace('  ',' ')
				i = i+1
			domain_file.write(question)
			domain_file.write('\n\n')
#			domain_file.write(str(objective))
#			domain_file.write('\n')
#			domain_file.write("|\n")
	domain_file.close()
	print(domain," is completed !")




	
	

#print(aptitude_topics.find_all('a'));

