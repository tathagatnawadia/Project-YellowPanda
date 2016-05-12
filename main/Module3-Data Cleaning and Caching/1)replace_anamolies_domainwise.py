'''

The aims for this module is to 

Phase 1

1.Read the unclean corpus ./corpus/*.store 
2.Do human replacement of human nature (Rs. -> Rs)

Phase 2

1.Identify the abbreviations in the domains using multiple combinations of regex
2.Display the abbreviations for the human to read
3.Replace the unique abbreviations with their typed replacement

Phase 3

1.Create another folder ./corpus/corrected
2.Recreate the clean corpus

'''

import os,re
import pickle

def removeMultipleNewLines(str):
	newstr = re.sub('\n+', '\n', str)
	return newstr

target_folder = os.path.join(os.getcwd(),'corpus')
print(target_folder)
print(" --------- Reading Corpus ------------")

file_dumps = {}
for i in os.listdir(target_folder):
	#For each domain file in the corpus open the file
	file_absolute_path = os.path.join(target_folder,i)
	#If the file is a .store file open and read the file
	if i.endswith(".store"): 
		'''
		file_dumps['Profit and Loss'] = "Question1\nQuestion2" and so on
		'''
		file_dumps[i] = open(file_absolute_path, "r").read()

print(" -------- Domains Activated ---------")
for key, value in file_dumps.items() :
	print(key,' -> ',len(file_dumps[key]), ' Questions.')
	

	
print(" -------- Correction Phase Starts --------- ")

'''
Specific corrections
'''

for key, value in file_dumps.items():
	temp = file_dumps[key]
	temp = temp.replace('Rs.','Rs ')
	temp = re.sub(r'\bhr\b', 'hour', temp)
	temp = re.sub(r'\bhrs\b', 'hours', temp)
	file_dumps[key] = temp
	
'''
Abbr corrections
'''

pattern_1 = re.compile("\s(?:(?<=\.|\s)[A-Za-z]\.)+\s") #Dotted Abbrevations r.p.m.
pattern_2 = re.compile("\s([A-Za-z](?:\.[A-Za-z])+)\s") #Dotted Abbrevations r.p.m
pattern_3 = re.compile("\s([A-Za-z]\.[A-Za-z])\s") #Dotted Abbrevations p.a
pattern_4 = re.compile("[A-Z]{2,3}") #Non dotted Abbrevations

regexes = "\s(?:(?<=\.|\s)[A-Za-z]\.)+\s", "\s([A-Za-z](?:\.[A-Za-z])+)\s", "\s([A-Za-z]\.[A-Za-z])\s", "[A-Z]{2,3}"

total_abbr = {}
for key,value in file_dumps.items():
	result_1 = re.findall(pattern_1, value)
	result_2 = re.findall(pattern_2, value)
	result_3 = re.findall(pattern_3, value)
	result_4 = re.findall(pattern_4, value)
	print("---------- DOMAIN : ",key," ------------")
	total_abbr[key] = result_1 + result_2 + result_3 + result_4
	total_abbr[key] = list(set(total_abbr[key]))
	
	#Removing noises like A. V. 
	noise_pattern_1 = re.compile("\s([A-Z]\.)\s")
	filtered = filter(lambda i: not noise_pattern_1.search(i), total_abbr[key] )
	filtered = [i for i in  total_abbr[key] if not noise_pattern_1.search(i)]
	total_abbr[key] = filtered
	

for key,value in total_abbr.items():
	print(" ------------ For Domain : ",key,", the identified abbrevations are ----------- ")
	print(value)
	
'''
SEARCH FOR PICKLE STARTS
'''
all_domain_correction = {} #This will be used for pickling
abbr_replacements = {} #This will be used to replace 

newdirectory = os.path.join(os.getcwd(),'corpus','abbr')
if not os.path.exists(newdirectory):
	print("Warning : Abbreviation Pickle not found !! Entering Manual Correction Mode")
	os.makedirs(newdirectory)
	
	'''
	MANUAL CORRECTION MODE STARTS
	'''

	print(" -------- Manual Correction Mode Activated --------- ")
	print("NOTE : If you don't provide any correction replacement, the abbreveation will be defaulted back to the original corpus !")
	print("Prompt1 : Complete Correction :: ")
	print("Prompt2 : Replacement Correction ::")

	for key,value in total_abbr.items():
		corrections = {}
		rep = {}
		print(" ------------ For Domain : ",key,", the identified abbrevations are ----------- ")
		for abbr in value:
			
			toast_message = 'Full form for  '+abbr+' :: '
			corrections[abbr.strip()] = input(toast_message)
			toast_message = 'Replacement form for  '+abbr+' :: '
			rep[abbr.strip()] = input(toast_message)
			
			if corrections[abbr.strip()] is '':
				corrections[abbr.strip()] = abbr.strip()
			if rep[abbr.strip()] is '':
				rep[abbr.strip()] = abbr.strip().replace('.','')
		
		all_domain_correction[key] = corrections
		abbr_replacements[key] = rep	
		
	#Start making pickle for caching the abbreviations at ./corpus/abbr.pickle

	full_form_pickle = os.path.join(os.getcwd(),'corpus','abbr','full_form.p')
	replacement_pickle = os.path.join(os.getcwd(),'corpus','abbr','replacement_form.p')

	pickle.dump( all_domain_correction, open( full_form_pickle, "wb" ) )
	pickle.dump( abbr_replacements, open( replacement_pickle, "wb" ) )

else:
	print("Success : Cached Pickles found !! Skipping Manual Correction Mode")
	full_form_pickle = os.path.join(os.getcwd(),'corpus','abbr','full_form.p')
	replacement_pickle = os.path.join(os.getcwd(),'corpus','abbr','replacement_form.p')

	all_domain_correction = pickle.load( open( full_form_pickle, "rb" ) )
	abbr_replacements = pickle.load( open( replacement_pickle, "rb" ) )

'''
-------------------------------------------------------------------------------------------------------------------------------------
'''

#all_domain_correction = {'ratio_and_proportion.store': {'A.B': 'A.B', 'L.C.M.': 'lowest common factor', 'S.I.': 'simple interest', 'T.V.': 'television'}, 'trains.store': {'a.m.': 'am'}, 'area_volume.store': {'AC': 'AC', 'ABC': 'ABC', 'm.': 'meter'}, 'simple_interest.store': {'p.a': 'per annum', 'SI': 'simple interest', 'CI': 'compound interest', 'R.D.': 'R.D.', 'p.a.': 'per annum', 'S.I.': 'simple interest'}, 'profit_loss.store': {'S.P.': 'selling price', 'C.P': 'cost price', 'IF': 'IF', 'ITC': 'ITC', 'DVD': 'DVD', 'S.P': 'selling price', 'T.V.s': 'televisions', 'T.V.': 'T.V.', 'C.P.': 'cost price', 'TV': 'TV'}, 'time_and_distance.store': {'a.m.': 'am', 'a.m': 'am', 'm.': 'meter', 'NH': 'NH', 'p.m.': 'pm', 'P.M.': 'pm'}, 'age.store': {'C.Q': 'C.Q'}, 'average.store': {'AB': 'AB', 'g.': 'gram', 'n.': 'n.', 'BA': 'BA', 'ODI': 'ODI'}}
#abbr_replacements = {'profit_loss.store': {'S.P': 'SP', 'S.P.': 'SP', 'T.V.s': 'TVs', 'TV': 'TV', 'IF': 'IF', 'ITC': 'ITC', 'DVD': 'DVD', 'C.P.': 'CP', 'T.V.': 'TV', 'C.P': 'CP'}, 'trains.store': {'a.m.': 'AM'}, 'area_volume.store': {'m.': 'meter', 'ABC': 'ABC', 'AC': 'AC'}, 'ratio_and_proportion.store': {'S.I.': 'SI', 'L.C.M.': 'LCM', 'T.V.': 'TV', 'A.B': 'A.B'}, 'simple_interest.store': {'p.a.': 'PA', 'SI': 'SI', 'R.D.': 'RD', 'p.a': 'PA', 'S.I.': 'SI', 'CI': 'CI'}, 'average.store': {'BA': 'BA', 'ODI': 'ODI', 'n.': 'n.', 'AB': 'AB', 'g.': 'gram'}, 'time_and_distance.store': {'m.': 'meter', 'a.m.': 'AM', 'p.m.': 'PM', 'NH': 'NH', 'a.m': 'AM', 'P.M.': 'PM'}, 'age.store': {'C.Q': 'C.Q'}}
#
#
#full_form_pickle = os.path.join(os.getcwd(),'corpus','abbr','full_form.p')
#replacement_pickle = os.path.join(os.getcwd(),'corpus','abbr','replacement_form.p')
#os.unlink(full_form_pickle)
#os.unlink(replacement_pickle)
#
#pickle.dump( all_domain_correction, open( full_form_pickle, "wb" ) )
#pickle.dump( abbr_replacements, open( replacement_pickle, "wb" ) )
print(" ------------------ Applying abbreviation corrections -----------------")
#print(all_domain_correction)
#print(abbr_replacements)


for domain,corrections in abbr_replacements.items():
	temp = file_dumps[domain]
	for abbr,replace in corrections.items():
		print(abbr,' -> ',replace)
		pattern = r'\b'+re.escape(abbr)+r'?(?!\S)'
		temp = re.sub(pattern, replace, temp)
		temp = re.sub(' +',' ',temp)
	file_dumps[domain] = temp
	

print(" --------- Making a seperate correction folder ---------- ")

newdirectory = os.path.join(os.getcwd(),'corpus','corrected')
if not os.path.exists(newdirectory):
	os.makedirs(newdirectory)
else:
	print("Folder Already Exists, Truncating Folder ......... ")
	for dirfile in os.listdir(newdirectory): 
		file_path = os.path.join(newdirectory, dirfile)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
		except Exception as e:
			print(e)



'''
Writing back corrected files 
'''
for key, value in file_dumps.items():
	domain_file_name = newdirectory+"/"+key
	domain_file = open(domain_file_name, 'w')
	print("Creating Corrected Files for ",key," .... ")
	domain_file.write(value)
	domain_file.close()
