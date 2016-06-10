import nltk
from nltk import *
import sympy
from sympy import *
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
import string
import re


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

def FindObjective(text) :
    e=[]
    Objectivelist={}
    t=text
    token=nltk.word_tokenize(t)
    tagged=nltk.pos_tag(token)
    e = [e for e in tagged if e[1] in ["NN","NNS"]]
    for o in e:
        if o[0] in ["length","time","speed"]:
            Objectivelist['attribute']=o[0]
        if o[0] in ["train","Train"]:
            Objectivelist['Obj']='train'
        if o[0] in ["jogger","Jogger"]:
            Objectivelist['Obj']='jogger'
        if o[0] in ["platform","Platform","bridge","Bridge"]:
            Objectivelist['Obj']='platform'
        if o[0] in ["pole","Pole","tree","Tree"]:
            Objectivelist['Obj']='pole'
    return Objectivelist

def train_jogger(Objectivelist) :
    
    tlength, tspeed, jogtime, jogspeed=symbols('tlength tspeed jogtime jogspeed')
    if direct == 1:
        expr=Eq(tlength/jogtime,tspeed-jogspeed)
    if direct == -1:
        expr=Eq(tlength/jogtime,tspeed+jogspeed)
    dictatt={}
    setl={}
    setl['tlength']=setl['tspeed']=setl['jogtime']=setl['jogspeed']=0
    
    tspeed=trainobj.speed
    if(tspeed!=999):
        searchobj=re.search(r'([0-9]+)([a-z]+/?[a-z]+)',tspeed,re.I)
        unit=searchobj.group(2)
        #print (unit)
        snum=searchobj.group(1)
        #print(snum)
        if unit in ["meters/second","meter/second","m/s","m/sec","meters/sec","meter/sec"]:
            snum=float(snum)*18/5
        if unit in ["meters/minute","meters/min","meter/minute","meter/min"]:
            snum=float(snum)*3/50
        #if unit in ["miles/second","mile/second","mile/sec","mile/s","miles/sec","miles/s"]:
        #   num=float(num)*
        dictatt['tspeed']=snum
        setl['tspeed']=1
        #print(snum)
    
    tlength=trainobj.length
    if(tlength!=999):
        searchobj=re.search(r'([0-9]+)([a-z]+)',tlength,re.I)
        unit=searchobj.group(2)
        #print(unit)
        dnum=searchobj.group(1)
        #print(dnum)
        if unit in ["meters","meter","m"]:
            dnum=float(dnum)/1000
        if unit in ["mile","miles"]:
            dnum=float(dnum)*1000000/621371
        dictatt['tlength']=dnum
        setl['tlength']=1
        #print(dnum)
    
    jogtime=jogobj.time
    if(jogtime!=999):
        searchobj=re.search(r'([0-9]+)([a-z]+)',jogtime,re.I)
        unit=searchobj.group(2)
        #print(unit)
        tnum=searchobj.group(1)
        #print(tnum)
        if unit in ["seconds","sec","second","s"]:
            tnum=float(tnum)/3600
        if unit in ["minutes","minute","min"]:
            tnum=float(tnum)/60
        dictatt['jogtime']=tnum
        setl['jogtime']=1
        #print(tnum)
    
    jogspeed=jogobj.speed
    if(jogspeed!=999):
        searchobj=re.search(r'([0-9]+)([a-z]+/?[a-z]+)',jogspeed,re.I)
        unit=searchobj.group(2)
        #print(unit)
        jsnum=searchobj.group(1)
        #print(jsnum)
        if unit in ["meters/second","meter/second","m/s","m/sec","meters/sec","meter/sec"]:
            jsnum=float(jsnum)*18/5
        if unit in ["meters/minute","meters/min","meter/minute","meter/min"]:
            jsnum=float(jsnum)*3/50
        dictatt['jogspeed']=jsnum
        setl['jogspeed']=1
        #print(jsnum)

    for k in setl.keys():
        if setl[k] == 0 :
            tofind = k
    
    temp=expr
    for k,v in dictatt.items():
        temp=temp.subs(k,v)

    res=solve(temp,tofind)

    if tofind == "tlength" :
        trainobj.length = repr(res) + "km"
        print(trainobj.length)
    if tofind == "tspeed" :
        trainobj.speed = repr(res) + "km/hr"
        print(trainobj.speed)
    if tofind == "jogtime":
        jogobj.time = repr(res) + "hr"
        print(jogobj.time)
    if tofind == "jogspeed":
        jogobj.speed = repr(res) + "km/hr"
        print(jogobj.speed)

    #print (res)

def plat_pole(Objectivelist):
    tlength, tspeed, plattime, platlength,poletime=symbols('tlength tspeed plattime platlength poletime')
    expr1=Eq(tlength/poletime,(platlength+tlength)/plattime)
    expr2=Eq(tlength/poletime,tspeed)
    tofind="tlength"
    dictatt={}
    #attset = {}
    #attset['tlength']=attset['tspeed']=attset['plattime']=attset['platlength']=0
    
    
    
    plattime=platobj.time
    searchobj=re.search(r'([0-9]+)([a-z]+)',plattime,re.I)
    unit=searchobj.group(2)
    #print(unit)
    tnum=searchobj.group(1)
    #print(tnum)
    if unit in ["seconds","sec","second","s"]:
        tnum=float(tnum)/3600
    if unit in ["minutes","minute","min"]:
        tnum=float(tnum)/60
    dictatt['plattime']=tnum
    #attset['plattime']=1
    #print(tnum)
    
    platlength=platobj.length
    searchobj=re.search(r'([0-9]+)([a-z]+)',platlength,re.I)
    unit=searchobj.group(2)
    #print(unit)
    pdnum=searchobj.group(1)
    #print(pdnum)
    if unit in ["meters","meter","m"]:
        pdnum=float(pdnum)/1000
    if unit in ["mile","miles"]:
        pdnum=float(pdnum)*1000000/621371
    dictatt['platlength']=pdnum
    #attset['platlength']=1

    #print (attset)
    poletime=poleobj.time
    searchobj=re.search(r'([0-9]+)([a-z]+)',poletime,re.I)
    unit=searchobj.group(2)
    #print(unit)
    tnum=searchobj.group(1)
    #print(tnum)
    if unit in ["seconds","sec","second","s"]:
        tnum=float(tnum)/3600
    if unit in ["minutes","minute","min"]:
        tnum=float(tnum)/60
    dictatt['poletime']=tnum

    #print(tofind)
    
    temp=expr1
    for k,v in dictatt.items():
        temp=temp.subs(k,v)
    print(temp)
    res=solve(temp,tofind)
    
    #print("tlength")
    if tofind == "tlength" :
        trainobj.length = repr(res[0])+"km"
        print(trainobj.length)
        num=res[0]*1000
        print(repr(num)+"meters")
        
    print("train obj length",trainobj.length)    
    dictatt={}
    
    poletime=poleobj.time
    searchobj=re.search(r'([0-9]+)([a-z]+)',poletime,re.I)
    unit=searchobj.group(2)
    #print(unit)
    tnum=searchobj.group(1)
    #print(tnum)
    if unit in ["seconds","sec","second","s"]:
        tnum=float(tnum)/3600
    if unit in ["minutes","minute","min"]:
        tnum=float(tnum)/60
    dictatt['poletime']=tnum
    
    tlength=trainobj.length
    searchobj=re.search(r'([0-9]+.[0-9]+)([a-z]+)',tlength,re.I)
    unit=searchobj.group(2)
    #print(unit)
    pdnum=searchobj.group(1)
    #print(pdnum)
    dictatt['tlength']=pdnum
    
    tofind="tspeed"
    
    temp=expr2
    for k,v in dictatt.items():
        temp=temp.subs(k,v)
    #print(temp)
    res=solve(temp,tofind)
    
    if tofind == "tspeed" :
        trainobj.speed = repr(res[0]) + "km/hr"
        print("Train obj speed",trainobj.speed)
        num=res[0]*5/18
        print(repr(num)+"m/sec")
    
    


def train_platform(Objectivelist):
    tlength, tspeed, plattime, platlength=symbols('tlength tspeed plattime platlength')
    expr=Eq(tspeed*plattime,tlength+platlength)
    dictatt={}
    attset = {}
    attset['tlength']=attset['tspeed']=attset['plattime']=attset['platlength']=0
    
    tspeed=trainobj.speed
    if(tspeed != 999):
        searchobj=re.search(r'([0-9]+.?[0-9]+)([a-z]+/*[a-z]+)',tspeed,re.I)
        unit=searchobj.group(2)
        #print(unit)
        snum=searchobj.group(1)
        #print(snum)
        if unit in ["meters/second","meter/second","m/s","m/sec","meters/sec","meter/sec"]:
            snum=float(snum)*18/5
        if unit in ["meters/minute","meters/min","meter/minute","meter/min"]:
            snum=float(snum)*3/50
        #if unit in ["miles/second","mile/second","mile/sec","mile/s","miles/sec","miles/s"]:
        #   num=float(num)*
        dictatt['tspeed']=snum
        attset['tspeed']=1
        #print(snum)
    
    tlength=trainobj.length
    if(tlength!= 999):
        searchobj=re.search(r'([0-9]+)([a-z]+)',tlength,re.I)
        unit=searchobj.group(2)
        #print(unit)
        dnum=searchobj.group(1)
        #print(dnum)
        if unit in ["meters","meter","m"]:
            dnum=float(dnum)/1000
        if unit in ["mile","miles"]:
            dnum=float(dnum)*1000000/621371
        dictatt['tlength']=dnum
        attset['tlength']=1
    #print(dnum)
    
    plattime=platobj.time
    if(plattime!= 999):
        searchobj=re.search(r'([0-9]+)([a-z]+)',plattime,re.I)
        unit=searchobj.group(2)
        #print(unit)
        tnum=searchobj.group(1)
        #print(tnum)
        if unit in ["seconds","sec","second","s"]:
            tnum=float(tnum)/3600
        if unit in ["minutes","minute","min"]:
            tnum=float(tnum)/60
        dictatt['plattime']=tnum
        attset['plattime']=1
    #print(tnum)
    
    platlength=platobj.length
    if(platlength!= 999):
        searchobj=re.search(r'([0-9]+)([a-z]+)',platlength,re.I)
        unit=searchobj.group(2)
        #print(unit)
        pdnum=searchobj.group(1)
        #print(pdnum)
        if unit in ["meters","meter","m"]:
            pdnum=float(pdnum)/1000
        if unit in ["mile","miles"]:
            pdnum=float(pdnum)*1000000/621371
        dictatt['platlength']=pdnum
        attset['platlength']=1

    #print (attset)

    for k,v in attset.items():
        if attset[k] == 0 :
            tofind = k

    #print(tofind)
    
    temp=expr
    for k,v in dictatt.items():
        temp=temp.subs(k,v)
    print(temp)
    res=solve(temp,tofind)
   
    if tofind == "tlength" :
        trainobj.length = repr(res[0])+"km"
        print(trainobj.length)
        num=res[0]*1000
        print(repr(num)+"meters")
    if tofind == "tspeed" :
        trainobj.speed = repr(res[0]) + "km/hr"
        print(trainobj.speed)
        num=res[0]*5/18
        print(repr(num)+"m/sec")
    if tofind == "plattime":
        platobj.time = repr(res[0]) + "hr"
        print(platobj.time)
        num=res[0]*60
        print(repr(num)+"minutes")
        num=res[0]*3600
        print(repr(num)+"seconds")
    if tofind == "platlength":
        platobj.length = repr(res[0])+"km"
        print(platobj.length)
        num=res[0]*1000
        print(repr(num)+"meters")
    
def train_pole(Objectivelist) :
    tlength, tspeed, poletime=symbols('tlength tspeed poletime')
    expr=Eq(tspeed*poletime,tlength)
    dictatt={}
    attset={}
    attset['tlength']=attset['tspeed']=attset['poletime']=0
    
    tspeed=trainobj.speed
    if(tspeed!=999):
        searchobj=re.search(r'([0-9]+)([a-z]+/*[a-z]+)',tspeed,re.I)
        unit=searchobj.group(2)
        #print(unit)
        snum=searchobj.group(1)
        #print(snum)
        if unit in ["meters/second","meter/second","m/s","m/sec","meters/sec","meter/sec"]:
            snum=float(snum)*18/5
        if unit in ["meters/minute","meters/min","meter/minute","meter/min"]:
            snum=float(snum)*3/50
        #if unit in ["miles/second","mile/second","mile/sec","mile/s","miles/sec","miles/s"]:
        #   num=float(num)*
        dictatt['tspeed']=snum
        attset['tspeed']=1
        #print(snum)
    
    tlength=trainobj.length
    if(tlength!=999):
        searchobj=re.search(r'([0-9]+)([a-z]+)',tlength,re.I)
        unit=searchobj.group(2)
        #print(unit)
        dnum=searchobj.group(1)
        #print(dnum)
        if unit in ["meters","meter","m"]:
            dnum=float(dnum)/1000
        if unit in ["mile","miles"]:
            dnum=float(dnum)*1000000/621371
        dictatt['tlength']=dnum
        attset['tlength']=1
    #print(dnum)
    
    poletime=poleobj.time
    if(poletime!=999):
        searchobj=re.search(r'([0-9]+)([a-z]+)',poletime,re.I)
        unit=searchobj.group(2)
        #print(unit)
        tnum=searchobj.group(1)
        #print(tnum)
        if unit in ["seconds","sec","second","s"]:
            tnum=float(tnum)/3600
        if unit in ["minutes","minute","min"]:
            tnum=float(tnum)/60
        dictatt['poletime']=tnum
        attset['poletime']=1
    #print(tnum)
    
    #print(attset)
    
    for key,value in attset.items():
        if value == 0 :
            tofind = key
    
    temp=expr
    for k,v in dictatt.items():
        temp=temp.subs(k,v)

    res=solve(temp,tofind)

    if tofind == "tlength" :
        trainobj.length = repr(res[0]) + "km"
        print(trainobj.length)
        num=res[0]*1000
        print(repr(num)+"meters")
    if tofind == "tspeed" :
        trainobj.speed = repr(res[0]) + "km/hr"
        print(trainobj.speed)
        num=res[0]*5/18
        print(repr(num)+"m/sec")
    if tofind == "poletime":
        poleobj.time = repr(res[0]) + "hr"
        print(poleobj.time)
        num=res[0]*60
        print(repr(num)+"minutes")
        num=res[0]*3600
        print(repr(num)+"seconds")

    



def compute_trains(finalobjlist,Objectivelist) :
    unk1=unk2=upole=uplat=0
    strobj=""
    for e in finalobjlist:
        strobj=strobj+e
    #print(strobj)
    if strobj in ["trainpole","poletrain"] :
        train_pole(Objectivelist)
    if strobj in ["trainplatform","platformtrain"] :
        train_platform(Objectivelist)
    if strobj in ["trainjogger","joggertrain"] :
        train_jogger(Objectivelist)
        
    if re.search(r'train',strobj) != None and re.search(r'pole',strobj) != None and re.search(r'platform',strobj) != None :
        if Objectivelist['Obj'] == "pole" :
            train_platform(Objectivelist)
            train_pole(Objectivelist)
        elif Objectivelist['Obj'] == "platform" :
            train_pole(Objectivelist)
            train_platform(Objectivelist)
        else :
            if poleobj.time!=999:
                upole=upole+1
            if platobj.length!=999:
                uplat=uplat+1
            if platobj.time!=999:
                uplat=uplat+1
            print(upole)
            print(uplat)
            if upole==uplat :
                train_pole(Objectivelist)
                train_platform(Objectivelist)
            if upole==0 :
                train_platform(Objectivelist)
                train_pole(Objectivelist)
            if upole==1 and uplat==2:
                plat_pole(Objectivelist)
            
    if re.search(r'train',strobj) != None and re.search(r'pole',strobj) != None and re.search(r'jogger',strobj) != None :
        if Objectivelist['Obj'] == "pole" :
            train_jogger(Objectivelist)
            train_pole(Objectivelist)
        elif Objectivelist['Obj'] == "jogger" :
            train_pole(Objectivelist)
            train_jogger(Objectivelist)
        else :
            if poleobj.time==999:
                upole=upole+1
            if jogobj.time==999:
                ujog=ujog+1
            if jogobj.speed==999:
                ujog=ujog+1
            if upole==ujog:
                train_pole(Objectivelist)
                train_jogger(Objectivelist)
            if upole==0:
                train_jogger(Objectivelist)
                train_pole(Objectivelist)
            if upole==1 and ujog==2 :
                jog_pole(Objectivelist)
            
    if re.search(r'train',strobj) != None and re.search(r'jogger',strobj) != None and re.search(r'platform',strobj) != None :
        if Objectivelist['Obj'] == "jogger" :
            train_platform(Objectivelist)
            train_jogger(Objectivelist)
        elif Objectivelist['Obj'] == "platform" :
            train_jogger(Objectivelist)
            train_platform(Objectivelist)
        else :
            if jogobj.time == 999 :
                unk1=unk1+1
            if jogobj.speed == 999 :
                unk1=unk1+1
            if platobj.time == 999 :
                unk2=unk2+1
            if platobj.length == 999 :
                unk2=unk2+1
            if unk1 > unk2 :
                train_platform(Objectivelist)
                train_jogger(Objectivelist)
            if unk2 > unk1 :
                train_jogger(Objectivelist)
                train_platform(Objectivelist)
                
            
    
    
    
def nlp_trains(t) :
    #text="A train 130 metres long and a travelling at 45 km/hr can cross a bridge in 30 seconds.What is the length of the bridge"
    text=t
    textlist=re.split(r'[,.]',text)
    n=len(textlist)

    Objectivelist=FindObjective(textlist[n-1])
    print("The Objective of the question is to find ",Objectivelist,"\n")

    i=0
    tlist=[]
    while i<n-1 :
        tlist.append(textlist[i])
        i=i+1
    tlist=" ".join(tlist)
    #print(tlist)

    swords=set(stopwords.words('english'))
    swlist=[]
    for l in swords:
        if l != "same" and l != "each" and l != "equal" and l != "m" and l != "min":
            swlist.append(l)

    punct=set(string.punctuation)

    unit={}
    unit['meters']=unit['meter']=unit['kilometer']=unit['m']=unit['km']="length"
    unit['minutes']=unit['hours']=unit["seconds"]=unit['min']=unit['sec']=unit['s']=unit['hrs']=unit['hr']="time"
    unit['kmph']=unit['km/hr']=unit['m/sec']=unit['m/s']="speed"

    objlist=["train","Train","Trains","man","Man","Jogger","jogger","pole","Pole","platform","Platform","bridge","tunnel","Tunnel"]


    words=nltk.word_tokenize(tlist)
    tag=nltk.pos_tag(words)
    l=[l for l in tag if l[0] not in swlist]
    r1=[r for r in l if r[0] not in punct]    
    #print(r1)
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
    #print(r3)
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
        if (r3[j])[0]+(r3[j+1])[0] in ["manrunning","ManRunning","manwalking","ManWalking"] :
            r3=r3[:j]+[("jogger","OBJ")]+r3[j+2:]
        j=j+1
    #print(r3,'\n')
    
    textlist=""
    for r in r3:
        textlist=textlist+r[0]
    
    global direct
    direct=0
    m=re.search('oppositedirection|directionopposite',textlist)
    if m != None :
        direct=-1
    m=re.search('samedirection',textlist)
    if m != None:
        direct=1
    print('direct = ',direct,'\n')
    r3=[r for r in r3 if r[1] in ["OBJ","CD","NN","NNS"]]
    
    chunkGrammar=r"""OBJ:{<OBJ>}
    VALUE:{<CD><NNS>|<CD><NN>}
    ATT:{<NN><VALUE>}
    """
    chunkParser=nltk.RegexpParser(chunkGrammar)
    chunked=chunkParser.parse(r3)
    chunked.draw()
    #print(chunked)


    finalobj={}
    finalobjlist=[]
    from nltk import Tree
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
                if (n[0])[0] in ["platform","Platform","bridge","Bridge","tunnel","Tunnel"]:
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
                if (n[0])[0] in ["platform","Platform","bridge","Bridge","tunnel","Tunnel"]:
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
    print("Final Object List ",finalobj,'\n')

    for e in finalobj.keys():
        if e == "train":
            global trainobj
            trainobj=Train()
            for at in finalobj[e]:
                if (at[0])[0] == "length":
                    val=(at[1])[0]+(at[2])[0]
                    print(val)
                    #print((at[1])[0])
                    #print((at[2])[0])
                    trainobj.length=val
                if (at[0])[0] == "speed":
                    val=(at[1])[0]+(at[2])[0]
                    #print(val)
                    trainobj.speed=val
       
        if e == "jogger":
            global jogobj
            jogobj=Jogger()
            for at in finalobj[e]:
                if (at[0])[0] == "speed":
                    val=(at[1])[0]+(at[2])[0]
                    #print(val)
                    jogobj.speed=val
                if (at[0])[0] == "time":
                    val=(at[1])[0]+(at[2])[0]
                    #print(val)
                    jogobj.time=val
        
        if e == "platform":
            global platobj
            platobj=Platform()
            for at in finalobj[e]:
                if (at[0])[0] == "length":
                    val=(at[1])[0]+(at[2])[0]
                    #print(val)
                    platobj.length=val
                if (at[0])[0] == "time":
                    val=(at[1])[0]+(at[2])[0]
                    #print(val)
                    platobj.time=val
       
        if e == "pole":
            global poleobj
            poleobj=Pole()
            for at in finalobj[e]:
                if (at[0])[0] == "time":
                    val=(at[1])[0]+(at[2])[0]
                    #print(val)
                    poleobj.time=val
        
   
    
    compute_trains(finalobjlist,Objectivelist)

while True:
    text = input('Question : ')
    if text == 'exit':
        break
    nlp_trains(text)
