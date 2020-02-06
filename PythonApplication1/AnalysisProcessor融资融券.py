from RClient import RClient
import json
from CONVERTOR import CONVERT
from CHECKER import CHECKER 
import jieba
from numpy import *

r=RClient.GetInst()

def 连续N天流入或流出的股(arr,dayCount=4):
    arr = sorted(arr,  key  = lambda  k:k["交易日期Tag"],reverse=True)
    size = len(arr)
    dayCount = dayCount if dayCount<size else size
    subArr = arr[:dayCount]
    subArr融资净买入=list(map(lambda x:x["融资净买入"],subArr))
    subArr融资净买入中位数 = median(subArr融资净买入)
    find=True
    for item in subArr:
        if item["融资净买入"]>0:
            #print("%s %s %s"%(item["Code"],item["交易日期"],item["融资净买入"]))
            find=find and False
            break
        elif  item["融资净买入"]==0: 
            find=find and False
            break
        elif  item["融资净买入"]<0 and subArr融资净买入中位数<0: 
            find=find and True
    return find
    pass

def FindTarget(code,arr):
    arr = list(map(lambda x:json.loads(x),arr))
    res = 连续N天流入或流出的股(arr) 
    if True  == res:
        print("%s %s"%(arr[0]["Code"],arr[0]["Name"]))
    pass

def AnalysisList1(arr,startIndex=0,size=20):
    arr = list(map(lambda x:json.loads(x),arr))
    arr = sorted(arr,  key  = lambda  k:k["交易日期Tag"],reverse=True)
    size = len(arr)
    step3=3
    step5=5
    step10=10
    cur=0
    while cur<size: 
        section3= arr[cur:cur+step3 if cur+step3<size else -1]
        section3融资余额占流通市值比=list(map(lambda x:x["融资余额占流通市值比"],section3))
        section3融资余额占流通市值比中位数 = median(section3融资余额占流通市值比)

        section5= arr[cur:cur+step5 if cur+step5<size else -1]
        section5融资余额占流通市值比=list(map(lambda x:x["融资余额占流通市值比"],section5))
        section5融资余额占流通市值比中位数 = median(section5融资余额占流通市值比)

        section10= arr[cur:cur+step10 if cur+step10<size else -1]
        section10融资余额占流通市值比=list(map(lambda x:x["融资余额占流通市值比"],section10))
        section10融资余额占流通市值比中位数 = median(section10融资余额占流通市值比)
        
        cur+=1
    pass



def callback(code):  
    #print(code)
    keyName = "PreData:股票:%s:融资融券"%code
    arr=  r.SortDictGetMax(keyName)
    if [] !=arr: 
        FindTarget(code,arr)
        #AnalysisList(arr)
        #if 0<len(arr):
        #    data =  json.loads(arr[0] ) 
        #    code = data["Code"]
        #    name = data["Name"]
            #dateTag = data["DateTag"]
            #print(data)
    pass
_keys  =r.DictKeys("AnalysisData:AllStockCode")
for _key in _keys :
    callback(_key)
print("OK")