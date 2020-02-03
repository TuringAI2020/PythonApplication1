from RClient import RClient
import json
from CONVERTOR import CONVERT
from CHECKER import CHECKER 

r=RClient.GetInst()

def callback(item): 
    code = item.split(":")[2]
    dictName="AnalysisData:AllStockCode"
    r.DictSave(dictName,code,code)
    pass
_keys  =r.QueryKeys("PreData:股票:*")
for key in _keys[1] :
    callback(key)
print("OK")