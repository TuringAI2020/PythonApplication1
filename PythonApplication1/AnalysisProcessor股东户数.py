from RClient import RClient
import json
from CONVERTOR import CONVERT
from CHECKER import CHECKER 
import jieba

r=RClient.GetInst()

def callback(code):  
    #print(code)
    keyName = "PreData:股票:%s:股东户数"%code
    arr=  r.SortDictGetMax(keyName)
    if [] !=arr:
        for item in arr:
            data = json.loads(item)
            code = data["Code"]
            name = data["Name"]
            #dateTag = data["DateTag"]
            print(item)
    pass
_keys  =r.DictKeys("AnalysisData:AllStockCode")
for key in _keys :
    callback(key)
print("OK")