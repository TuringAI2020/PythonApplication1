from RClient import RClient
import json
from CONVERTOR import CONVERT
from CHECKER import CHECKER 
import jieba

r=RClient.GetInst()

def callback(code):  
    #print(code)
    keyName = "PreData:股票:%s:机构调研"%code
    arr=  r.SortDictGetMax(keyName)
    if [] !=arr:
        arr = sorted(arr,  key  = lambda  k:json.loads(k)["公告日期Tag"],reverse=True)
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