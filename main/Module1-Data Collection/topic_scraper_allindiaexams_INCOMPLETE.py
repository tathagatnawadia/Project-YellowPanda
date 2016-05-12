from pymongo import MongoClient
from bs4 import BeautifulSoup
import urllib.request

r = urllib.request.urlopen('http://www.allindiaexams.in/aptitude-questions-and-answers/pipes-and-cisterns').read()
soup = BeautifulSoup(r,"lxml")
furthur_links = []
next_links = soup.findAll("a", { "class" : "page" })
for link in next_links:
	href = link.get('href')
	furthur_links.append(href)
furthur_links = list(set(furthur_links))
print("Total Pages for the domain : ",len(furthur_links))

questions_div = soup.findAll("div", { "class" : "qa_list" })
print("Total questions in a single page : ",len(questions_div))
for question_div in questions_div:
	try:
		question = question_div.contents[2]
		print(question)
	except:
		print(" ----- It okay babe --- ")
	
	#options = question_div.findAll("ul",{ "class" : "options_list clearfix" })[0].findAll('li')
	

#print(list(set(furthur_links)))
#nohtml = soup.get_text()
#questions_div = soup.findAll("div", { "class" : "bix-div-container" })
#
#for question_div in questions_div:
#	#total_text = question_div.get_text();
#	objective = {}
#	i = 1
#	question = (question_div.findAll("td",{ "class" : "bix-td-qtxt" } ))[0].get_text().strip()
#	options = (question_div.findAll("table", { "class" : "bix-tbl-options" }))[0].findAll("td", {"class" : "bix-td-option", "width" : "49%"})
#	for option in options:
#		objective[i] = option.get_text()
#		i = i+1
#	print(question)
#	print(objective)
#	print("-------------------------")
##a = BeautifulSoup(questions,"lxml")
##
##questions = a.findAll("td", {"class" : "bix-td-qtxt"})
##for question in questions:
##	print(question)


	
	

#print(aptitude_topics.find_all('a'));

