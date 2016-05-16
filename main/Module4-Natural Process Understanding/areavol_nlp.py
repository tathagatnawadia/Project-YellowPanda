import nltk
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import *
import string
import queue
from objectivetimedistance import process_content
import nltk
import re
import sys
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
train_text=state_union.raw("2005-GWBush.txt")
q=None

def main():
    file_absolute_path = os.path.join(os.getcwd(),'corpus','corrected','area_volume.store')
    print(file_absolute_path)
    num_lines = sum(1 for line in open(file_absolute_path))
    f=open(file_absolute_path, 'r')
    j=0
    for j in range(0,num_lines):
        text=f.readline()
        
        #find the objective of the question
        process_content(text)
        
        #split the objective part of the function
        textlist=re.split(r'[,.]',text)
        n=len(textlist)
        i=0
        temp=""
        while i<n-1 :
         temp=temp+textlist[i]
         i=i+1
         
        #replace the measure words into numerical symbols
        tokens=nltk.word_tokenize(text)
        dict={}
        dict['Twice']=dict['twice']="2 *"
        dict['Thrice']=dict['thrice']="3 *"
        dict['Increased']=dict['increased']="+"
        dict['Decreased']=dict['decreased']="-"
        dict['Times']=dict['times']="*"
        dict['More']=dict['more']="+"
        dict['difference']= dict['Difference']="-"

        list=[]
        i=0
        for l in tokens:
         if l in dict.keys():
          list.append(dict[l])
         else:
          list.append(l)
          
        #part of speech tagger to find the object,attributes and value
        tag1=nltk.pos_tag(list)
        stop_words=set(stopwords.words('english'))
        r1=[r for r in tag1 if r[0] not in stop_words]
        punct=set(string.punctuation)
        final=[r for r in r1 if r[0] not in punct]
        dr=nltk.pos_tag(stop_words)
        sw=[]
        for l in dr:
         if l[1] not in ["DT","IN"]:
          sw.append(l)
        l=[]
        for s in sw:
         l.append(s[0])
        r1=[r for r in tag1 if r[0] not in l]

        punct=set(string.punctuation)
        final=[r for r in r1 if r[0] not in punct]

        chunkGrammar=r"""OBJ:{<JJ><NN>|<NN><NN>|<IN><DT><NN>}
        ATT:{<NN><IN>|<NN>|<NN><IN><DT><NN>}
        VALUE:{<CD><NNS>|<CD>}
        FIND:{<WP>}
        """
        chunkParser=nltk.RegexpParser(chunkGrammar)
        chunked=chunkParser.parse(r1)
        print(chunked)

        #process the chunked and differentiated parts as object,attributes to solve the problem
        # process_chunks(chunked)
        

if __name__=='__main__':
    main()
'''
------------------------------------------------------------------------------------------------------------------------------------------------------    

def process_chunks(chunked):
     global q=queue.Queue()
     for n in chunked:
        if isinstance(n,nltk.tree.Tree):
            if n.label() == 'OBJ':
                a=len(n)


                
            
            elif n.label() == 'ATT':
                q.put_nowait(n[0][0])
            elif n.label() == 'VALUE':
               q.put_nowait(n[0][0])
                
     return

 def make_keywords():
     i=0
     str=""
    for i in range(q.size()):
        str=str+q.get_nowait()
str=str+q.get_nowait()
        str=str+q.get_nowait()



class rectangle:
    def __init__(self):
        self.length=0
        self.width=0
        self.height=0
        self.area=0
        self.perimeter=0
        self.diagonal=0

    def assign_values(self,length,width,height,diagonal,perimeter):
        self.length=length
        self.width=width
        self.height=height
        self.diagonal=diagonal
        self.perimeter=perimeter

    def relation_attr(self,length,width,height,diagonal,area,perimeter):

'''



        
        

        
        
    
    

        
        
        
    
