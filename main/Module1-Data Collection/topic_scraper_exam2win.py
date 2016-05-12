from pymongo import MongoClient
from bs4 import BeautifulSoup
import urllib.request 
import os.path
import collections
import re
from json import *

doma={'simple-interest','profit-and-loss','problems-on-trains','problems-on-ages','average','time-and-distance','time-and-work','chain-rule','alligation-or-mixture','true-discount','problems-on-numbers','stocks-and-shares','calendar','area','pipes-and-cistern','ratio-and-proportion','compound-interest','partnership','clock','volume-and-surface-area','boats-and-streams','races-and-games'}

domains=sorted(doma)
'''
Getting all Domain Links and question storing them in dictionary
'''

domainquestion={}
finalquestion=[]
for domain in domains:
	print("Analysing -- ",domain," !!")
	for i in range(1,10):
		temp='http://exam2win.com/aptitude-test/'+str(domain)+'/question-papers-'+str(i)+'.jsp'
		r = urllib.request.urlopen(temp).read()
		soup=BeautifulSoup(r,"lxml")
		j=0
		for ntemp in soup.findAll("table"):
			faltu=ntemp.find("div",{"id":"pagenum"})
			value=ntemp.find("p")
			if faltu:
				continue
			elif j<3:
				tempques=value.b.get_text().strip()
				finalquestion=re.findall('[0-9]{1,2}\.(.*)',tempques)
				fquestion=finalquestion[0].lstrip()
			else:
				break
			j=j+1
			domainquestion.setdefault(domain,[]).append(fquestion)


for domain,questions in domainquestion.items():
	domain_file_name = "corpus/exam2win/"+domain+".store"
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


