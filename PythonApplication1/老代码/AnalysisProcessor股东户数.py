from RClient import RClient
import json
from CONVERTOR import CONVERT
from CHECKER import CHECKER 
import jieba

from numpy import *


r=RClient.GetInst()

def 连续N次股东户数减少(arr,count=1):
    currentDateTag = CONVERT.GetCurrentDateTag()
    arr = sorted(arr,  key  = lambda  k:k["股东户数统计截止日Tag"],reverse=True)
    size = len(arr)
    count = count if count<size else size
    subArr = arr[:count]
    subArr = list(filter(lambda k:k["股东户数统计截止日Tag"]>=currentDateTag-100,subArr)) #时间段要改进
    if 0== len(subArr):
        return False

    subArr股东户数增减比例=list(map(lambda x:x["股东户数增减比例"],subArr))
    subArr股东户数增减比例中位数 = median(subArr股东户数增减比例)
    find=True and 0<len(subArr)
    for item in subArr:
        #print("%s %s %s"%(arr[0]["Code"],arr[0]["Name"],item["股东户数增减比例"]))
        if item["股东户数增减比例"]>0: 
            find=find and False
            break
        elif  item["股东户数增减比例"]==0: 
            find=find and False
            break
        elif  item["股东户数增减比例"]<0 and subArr股东户数增减比例中位数<0: 
            find=find and True
    return find
    pass

def FindTarget(code,arr):
    arr = list(map(lambda x:json.loads(x),arr))
    res = 连续N次股东户数减少(arr) 
    if True  == res:
        print("%s %s"%(arr[0]["Code"],arr[0]["Name"]))
    pass

def callback(code):  
    #print(code)
    keyName = "PreData:股票:%s:股东户数"%code
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