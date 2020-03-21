from RClient import RClient
import json
from CONVERTOR import CONVERT
from CHECKER import CHECKER 
import jieba
from numpy import *


r=RClient.GetInst()

def 连续N次筹码集中度非常集中(arr,count=3):
    arr = sorted(arr,  key  = lambda  k:k["Tag"],reverse=True)
    size = len(arr)
    count = count if count<size else size
    subArr = arr[:count]
    subArr较上期变化=list(map(lambda x:x["较上期变化(%)"],subArr))
    subArr较上期变化中位数 = median(subArr较上期变化)
    find=True
    for item in subArr:
        if item["较上期变化(%)"]>0: 
            find=find and False
            break
        elif  item["较上期变化(%)"]==0: 
            find=find and False
            break
        elif  item["较上期变化(%)"]<0 and subArr较上期变化中位数<0: 
            find=find and True
    return find
    pass

def FindTarget(code,arr):
    arr = list(map(lambda x:json.loads(x),arr))
    res = 连续N次筹码集中度非常集中(arr) 
    if True  == res:
        print("%s %s"%(arr[0]["Code"],arr[0]["Name"]))
    pass

def callback(code):  
    #print(code)
    keyName = "PreData:股票:%s:股东研究"%code
    arr=  r.SortDictGetMax(keyName)
    if [] !=arr:
        FindTarget(code ,arr)
        #arr = sorted(arr,  key  = lambda  k:json.loads(k)["DateTag"],reverse=True)
        if 0<len(arr):
            data =  json.loads(arr[0] ) 
            code = data["Code"]
            name = data["Name"]
            #dateTag = data["DateTag"]
            #print(data)
    pass
_keys  =r.DictKeys("AnalysisData:AllStockCode")
for _key in _keys :
    callback(_key)
print("OK")