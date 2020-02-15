import os
import random
import time
import sys 
import io  #StringIO模块就是在内存中读写str
import re
import json  
from RClient import RClient
from CONVERTOR import CONVERT

r=RClient.GetInst()
 

def CreateTask北向成交明细(dictName,key,val,pageIndex,pageCount,pageSize,curIndex,total):
    code=key
    url = "http://data.eastmoney.com/hsgt/%s.html"%code #北向持股明细列表
    task={"Code":code,"Url":url,"RetryCount":3}
    taskID=CONVERT.StrToInt(code[len(code)-1])%4
    qName="Stock:Task:BXCJMX:Task%s"%taskID
    r.QueueEn(qName,json.dumps(task,ensure_ascii=False)) 
    print(curIndex)
    pass
r.DeleteKeys("Stock:Task:BXCJMX:*")
r.TraverseDict("Stock:BaseData:AllCode",CreateTask北向成交明细)
for k in range(4):
    r.DictSave("Stock:Task:BXCJMX:Status","Task%s"%k,0)
print("列表任务创建完毕")
time.sleep(10) 
print("OK") 