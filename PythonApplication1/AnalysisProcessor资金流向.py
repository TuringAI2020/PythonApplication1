from RClient import RClient
import json
from CONVERTOR import CONVERT
from CHECKER import CHECKER 

r=RClient.GetInst()

def callback(qName,input): 
    print("%s %s %s"%(qName,input[1],input[0]))
    data=json.loads(input[0])
    code = data["Code"].strip()
    name = data["Name"].strip()
 
    pass
_keys  =r.QueryKeys("PreData:股票:*:资金流向")
for key in _keys[1] :
    r.TraverseSortedSet(key,callback)
print("OK")