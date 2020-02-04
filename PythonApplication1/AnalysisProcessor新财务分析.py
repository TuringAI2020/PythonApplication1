from RClient import RClient
import json
from CONVERTOR import CONVERT
from CHECKER import CHECKER 
import jieba

r=RClient.GetInst()

def callback(code):  
    #print(code)
    keyName = "PreData:股票:%s:新财务分析"%code
    arr=  r.SortDictGetMax(keyName)
    if [] !=arr:
        arr = filter(lambda k:None != "每股指标" in json.loads(k),arr)
        arr = list(arr)
        arr = sorted(arr,  key  = lambda  k:json.loads(k)["每股指标Tag"],reverse=True)
        if 0<len(arr):
            data =  json.loads(arr[0] ) 
            code = data["Code"]
            name = data["Name"]
            #dateTag = data["DateTag"]
            print(data)
    pass
_keys  =r.DictKeys("AnalysisData:AllStockCode")
for _key in _keys :
    callback(_key)
print("OK")