import nltk
from nltk import *
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
import string
import sympy
from sympy import *
import re
from re import *
from nltk import Tree

class Train:
    def __init__(self):
        self.length=999
        self.speed=999

    def set_length(self,l):
        self.length=l
    
    def set_speed(self,s):
        self.speed=s
        
    def get_length(self):
        return self.length
        
    def get_speed(self):
        return self.speed

class Platform:
    def __init__(self):
        self.length=999
        self.time=999

    def set_length(self,l):
        self.length=l
    
    def set_time(self,t):
        self.time=t
        
    def get_length(self):
        return self.length
        
    def get_time(self):
        return self.time

class Pole:
    def __init__(self):
        self.time=999
        
    def set_time(self,t):
        self.time=t
        
    def get_time(self):
        return self.time

class Jogger:
    def __init__(self):
        self.time=999
        
    def set_speed(self,s):
        self.speed=s
    
    def set_time(self,t):
        self.time=t
   
    def get_speed(self):
        return self.speed  
    
    def get_time(self):
        return self.time


def train_platform(direct):
    tlength, tspeed, plattime, platlength=symbols('tlength tspeed plattime platlength')
    expr=Eq(tspeed*plattime,tlength+platlength)
    dictatt={}
    attset = {}
    attset['tlength']=attset['tspeed']=attset['plattime']=attset['platlength']=0
    
    tspeed=trainobj.speed
    if(tspeed):
        searchobj=re.search(r'([0-9]+)([a-z]+/[a-z]+)',speed,re.I)
        unit=searchobj.group(2)
        num=searchobj.group(1)
        if unit in ["metres/second","metre/second","m/s","m/sec","metres/sec","metre/sec"]:
            snum=float(num)*18/5
        if unit in ["metres/minute","metres/min","metre/minute","metre/min"]:
            snum=float(num)*3/50
        #if unit in ["miles/second","mile/second","mile/sec","mile/s","miles/sec","miles/s"]:
        #   num=float(num)*
        dictatt['tspeed']=snum
        attset['tspeed']=1
        #print(snum)
    
    tlength=trainobj.length
    if(tlength):
        searchobj=re.search(r'([0-9]+)([a-z]+)',dist,re.I)
        unit=searchobj.group(2)
        dnum=searchobj.group(1)
        if unit in ["metres","metre","m"]:
            dnum=float(dnum)/1000
        if unit in ["mile","miles"]:
            dnum=float(dnum)*1000000/621371
        dictatt['tlength']=dnum
        attset['tlength']=1
    #print(dnum)
    
    plattime=platobj.time
    if(plattime):
        searchobj=re.search(r'([0-9]+)([a-z]+)',time,re.I)
        unit=searchobj.group(2)
        tnum=searchobj.group(1)
        if unit in ["seconds","sec","second","s"]:
            tnum=float(tnum)/3600
        if unit in ["minutes","minute","min"]:
            tnum=float(tnum)/60
        dictatt['plattime']=tnum
        attset['plattime']=1
    #print(tnum)
    
    platlength=platobj.length
    if(platlength):
        searchobj=re.search(r'([0-9]+)([a-z]+)',dist,re.I)
        unit=searchobj.group(2)
        pdnum=searchobj.group(1)
        if unit in ["metres","metre","m"]:
            pdnum=float(pdnum)/1000
        if unit in ["mile","miles"]:
            pdnum=float(pdnum)*1000000/621371
        dictatt['pltlength']=pdnum
        attset['platlength']=1

    for k,v in attset.items():
        if attset[k] == 0 :
            tofind = k
    
    temp=expr
    for k,v in dictatt.items():
        temp=temp.subs(k,v)

    res=solve(temp,tofind)

    if tofind == "tlength" :
        trainobj.length = res + "km"
    if tofind == "tspeed" :
        trainobj.speed = res + "km/hr"
    if tofind == "plattime":
        platobj.time = res + "hr"
    if tofind == "platlength":
        platobj.length = res + "km"

    print (res)


def fun(t):
    text=t

    swords=set(stopwords.words('english'))
    swlist=[]
    for l in swords:
        if l != "same" and l != "each" and l != "equal":
            swlist.append(l)

    punct=set(string.punctuation)

    unit={}
    unit['metres']=unit['km']="length"
    unit['minutes']=unit['hours']=unit["seconds"]="time"
    unit['kmph']=unit['km/hr']="speed"

    objlist=["train","Train","Trains","man","Man","Jogger","jogger","pole","Pole","platform","Platform","bridge"]


    words=nltk.word_tokenize(text)
    tag=nltk.pos_tag(words)
    l=[l for l in tag if l[0] not in swlist]
    r1=[r for r in l if r[0] not in punct]    

    i=0
    n=len(r1)
    while i<=n :
        if (r1[i])[1]== "CD" and (r1[i+1])[0] in ["Trains","trains"] :
            i=i+2
        if ((r1[i])[1] == "CD" and (r1[i+1])[1] in ["NN","NNS"]):
            attr=(r1[i+1][0])
            at=unit[attr]
            if (r1[i-1])[0] != at  :
                r1[i:i]=[(at,"NN")]
                i=i+1
        i=i+1

    j=0
    r2=r1
    newlen=len(r2)
    while j<newlen:
        if (r2[j])[0] in objlist :
            r2=r2[:j]+[((r2[j])[0],"OBJ")]+r2[j+1:]
        j=j+1

    r3=r2
    print(r3)
    j=0
    newlen=len(r3)
    while j<newlen-4 :
        if (r3[j])[0]+(r3[j+1])[0]+(r3[j+2])[0] in ["manstandingplatform","ManStandingPlatform","manstandingbridge","ManStandingBridge"] :
            r3=r3[:j]+[("pole","OBJ")]+r3[j+3:]
        if (r3[j])[0]+(r3[j+1])[0]+(r3[j+2])[0] in ["manrunningplatform","ManRunningPlatform","manrunningbridge","ManRunningBridge"] :
            r3=r3[:j]+[("jogger","OBJ")]+r3[j+3:]
        j=j+1
    
    j=0
    newlen=len(r3)
    while j<newlen-2 :
        if (r3[j])[0]+(r3[j+1])[0] in ["manstandingplatform","ManStandingPlatform","manstandingbridge","ManStandingBridge"] :
            r3=r3[:j]+[("pole","OBJ")]+r3[j+2:]
        if (r3[j])[0]+(r3[j+1])[0] in ["manrunning","ManRunning"] :
            r3=r3[:j]+[("jogger","OBJ")]+r3[j+2:]
        j=j+1
    print(r3,'\n')

    textlist=""
    for r in r3:
        textlist=textlist+r[0]

    direct=0
    m=re.search('oppositedirection|directionopposite',textlist)
    if m != None :
        direct=-1
    m=re.search('samedirection',textlist)
    if m != None:
        direct=1
        
    r3=[r for r in r3 if r[1] in ["OBJ","CD","NN","NNS"]]

    chunkGrammar=r"""OBJ:{<OBJ>}
    VALUE:{<CD><NNS>|<CD><NN>}
    ATT:{<NN><VALUE>}
    """
    chunkParser=nltk.RegexpParser(chunkGrammar)
    chunked=chunkParser.parse(r3)
    print(chunked)
    finalobj={}
    finalobjlist=[]

    tup=()

    for n in chunked:
        if isinstance(n,nltk.tree.Tree):
            if n.label() == 'OBJ':
                if (n[0])[0] in ["train","Train"]:
                    obj="train"
                    if obj not in finalobjlist:
                        finalobjlist.append("train")
                if (n[0])[0] in ["man","Man","pole","Pole","tree","Tree"]:
                    obj="pole"
                    if obj not in finalobjlist:
                        finalobjlist.append("pole")
                if (n[0])[0] in ["platform","Platform","bridge","Bridge"]:
                    obj="platform"
                    if obj not in finalobjlist:   
                        finalobjlist.append("platform")
                if (n[0])[0] in ["jogger","Jogger"]:
                    obj="jogger"
                    if obj not in finalobjlist:
                        finalobjlist.append("jogger")

    for e in finalobjlist:
        finalobj[e]=[]
    
    for n in chunked:
        if isinstance(n,nltk.tree.Tree):
            if n.label() == 'OBJ':
                if (n[0])[0] in ["train","Train"]:
                    key="train"
                if (n[0])[0] in ["man","Man","pole","Pole","tree","Tree"]:
                    key="pole"
                if (n[0])[0] in ["platform","Platform","bridge","Bridge"]:
                    key="platform"
                if (n[0])[0] in ["jogger","Jogger"]:
                    key="jogger" 
            if n.label() == 'ATT':
                att=(n[0])
                n=n[1]
                cd=(n[0])
                unit=(n[1])
                tup=(att,cd,unit)
                finalobj[key].append(tup)

    for e in finalobj.keys():
        if e == "train":
            global trainobj
            trainobj=Train()
            for at in finalobj[e]:
                if (at[0])[0] == "length":
                    val=(at[1])[0]+(at[2])[0]
                    print(val)
                    print((at[1])[0])
                    print((at[2])[0])
                    trainobj.length=val
                if (at[0])[0] == "speed":
                    val=(at[1])[0]+(at[2])[0]
                    print(val)
                    trainobj.speed=val
   
        if e == "jogger":
            joggerobj=Jogger()
            for at in finalobj[e]:
                if (at[0])[0] == "speed":
                    val=(at[1])[0]+(at[2])[0]
                    print(val)
                    joggerobj.speed=val
                if (at[0])[0] == "time":
                    val=(at[1])[0]+(at[2])[0]
                    print(val)
                    joggerobj.time=val
    
        if e == "platform":
            global platobj
            platobj=Platform()
            for at in finalobj[e]:
                if (at[0])[0] == "length":
                    val=(at[1])[0]+(at[2])[0]
                    print(val)
                    platobj.length=val
                if (at[0])[0] == "time":
                    val=(at[1])[0]+(at[2])[0]
                    print(val)
                    platobj.time=val

        if e == "pole":
            poleobj=Pole()
            for at in finalobj[e]:
                if (at[0])[0] == "length":
                    val=(at[1])[0]+(at[2])[0]
                    print(val)
                    poleobj.length=val

    train_platform(direct)

t="A train 130 metres long and a travelling at 45 km/hr can cross a bridge in 30 seconds"
fun(t)