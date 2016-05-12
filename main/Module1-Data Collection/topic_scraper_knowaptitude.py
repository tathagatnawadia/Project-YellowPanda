from pymongo import MongoClient
from bs4 import BeautifulSoup
import urllib.request 
import os.path
import collections
import re
from json import *
import urllib.error
from operator import itemgetter  

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.indiabix

urlCollection = db.urlCollection
domains={'simple-interest':32,'profit-and-loss':21,'problems-on-trains':19,'problems-on-ages':22,'average':23,'permutation-and-combination':24,'h.c.f-and-l.c.m':25,'time-and-distance':31,'partnership':33,'calendar':34,'chain-rule':27,'probability':41,'compound-interest':44,'percentage':45,'ratio-and-proportion':50,'simplification':49}
_offset=[0,31,61,91]
_pageno=[0,1,2,3]
urllist={}
'''
Root of all Domains
'''
dom=sorted(domains)
for domain in dom:
	for i in range(0,4):
		offset = _offset[i]
		pageno = _pageno[i]
		if i == 0:
			temp = 'http://www.knowaptitude.in/questions/dumps/aptitude/arithmetic-aptitude/'+str(domain)+'?type=latest'
		else:
			temp = 'http://www.knowaptitude.in/ajax/Questions/dump_fetch/30/1/'+str(offset)+'/'+str(pageno)+'/4/'+str(domains[domain])+'/-1?type=latest'
		urllist.setdefault(domain,[]).append(temp)

'''
urllist : contains {'domain-name-1': [link1,link2, .. ], 'domain-name-2': [link1,link2, ....]}
'''
domain_questions={}
foption=[]
for domain_name in sorted(urllist):
	i=0
	for url in urllist[domain_name]:
		r = urllib.request.urlopen(url).read()
		soup=BeautifulSoup(r,"lxml")
		for temp_question in soup.findAll("div",{"class":"dump_question"}):
			if i==0:
				hquestion=temp_question.get_text().replace("\\r","").replace("\\n","").replace("\\t","").replace("\t","").replace("\\","")
				finalquestion=re.findall('[0-9]{1,2}\)(.*)',hquestion)
				fquestion=finalquestion[0].lstrip()
			else:
				hquestion=temp_question.get_text().replace("\\r","").replace("\\n","").replace("\\t","").replace("\t","").replace("\\","")
				finalquestion=re.findall('[0-9]??\)(.+?) A\.',hquestion)
				fquestion=finalquestion[0].lstrip()
			domain_questions.setdefault(domain_name,[]).append(fquestion)
		i=i+1
		
for domain,questions in domain_questions.items():
		domain_file_name = "corpus/knowaptitude/"+domain+".store"
		if os.path.isfile(domain_file_name):
			print("Skipping : ",domain)
			continue
		domain_file = open(domain_file_name, 'w')
		print("Creating Files for ",domain)
		for question in questions:
			domain_file.write(question)
			domain_file.write('\n\n')
		domain_file.close()
		print(domain," is completed !")