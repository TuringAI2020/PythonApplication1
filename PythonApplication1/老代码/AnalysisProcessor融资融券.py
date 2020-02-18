from RClient import RClient
import json
from CONVERTOR import CONVERT
from CHECKER import CHECKER 
import jieba
from numpy import *

r=RClient.GetInst()

def 连续N天流入或流出的股(arr,dayCount=3):
    arr = sorted(arr,  key  = lambda  k:k["交易日期Tag"],reverse=True)
    size = len(arr)
    dayCount = dayCount if dayCount<size else size
    subArr = arr[:dayCount]
    subArr融资净买入=list(map(lambda x:x["融资净买入"],subArr))
    subArr融资净买入中位数 = median(subArr融资净买入)
    find=True
    for item in subArr:
        if item["融资净买入"]>4000 and 6000<=subArr融资净买入中位数:
            find=find and True
        elif  item["融资净买入"]==0: 
            find=find and False
            break
        elif  item["融资净买入"]<0: 
            find=find and False
            break
        else:
            return False
    return find
    pass

def FindTarget(code,arr):
    arr = list(map(lambda x:json.loads(x),arr))
    res = 连续N天流入或流出的股(arr) 
    if True  == res:
        print("%s %s"%(arr[0]["Code"],arr[0]["Name"]))
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