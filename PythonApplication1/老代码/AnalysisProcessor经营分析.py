from RClient import RClient
import json
from CONVERTOR import CONVERT
from CHECKER import CHECKER 
import jieba

from numpy import *


r=RClient.GetInst()

def 最新盈利能力指标(arr,count=8):
    currentDateTag = CONVERT.GetCurrentDateTag()
    arr = sorted(arr,  key  = lambda  k:k["盈利能力指标ag"],reverse=True)
    size = len(arr)
    count = count if count<size else size
    subArr = arr[:count]
    subArr = list(filter(lambda k:k["盈利能力指标Tag"]>=	20190930,subArr)) #时间段要改进
    if 0== len(subArr):
        return False

    subArr加权净资产收益率=list(map(lambda x:x["加权净资产收益率(%)"],subArr))
    subArr主力净流入净占比中位数 = median(subArr主力净流入净占比)
    find=True and 0<len(subArr)
    for item in subArr:
        #print("%s %s %s"%(arr[0]["Code"],arr[0]["Name"],item["股东户数增减比例"]))
        if item["加权净资产收益率(%)"]>0: 
            find=find and False
            break
        elif  item["主力净流入净占比"]==0: 
            find=find and False
            break
        elif  item["主力净流入净占比"]<0 and subArr主力净流入净占比中位数<0: 
            find=find and True
    return find
    pass

def FindTarget(code,arr):
    arr = list(map(lambda x:json.loads(x),arr))
    res = 连续N天主力净流出(arr) 
    if True  == res:
        print("%s %s"%(arr[0]["Code"],arr[0]["Name"]))
    pass

def callback(code):  
    #print(code)
    keyName = "PreData:股票:%s:经营分析"%code
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