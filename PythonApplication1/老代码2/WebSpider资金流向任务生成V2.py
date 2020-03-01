import os
import random
import time
import sys
import gzip
import urllib
import io  #StringIO模块就是在内存中读写str
import re
import json 
from CHECKER import CHECKER 
from RClient import RClient
from CONVERTOR import CONVERT
import psutil

r=RClient.GetInst() 
def CreateTask资金流向(setName,item):
    code=item[0]
    url = "http://data.eastmoney.com/zjlx/%s.html"%code 
    threadCount=psutil.cpu_count(True)
    taskID=CONVERT.StrToInt(code[len(code)-1])%threadCount
    task={"Code":code,"Url":url,"RetryCount":3}
    qName="Stock:Task:ZJLX:Task%d"%taskID
    r.QueueEn(qName,json.dumps(task,ensure_ascii=False))
    print("CreateTask资金流向 %s"%code)
    pass

print("WebSpider资金流向任务生成V2")
r.DeleteKeys("Stock:Task:ZJLX:*")
#r.TraverseDict("Stock:BaseData:AllCode",CreateTask资金流向)
r.TraverseSortedSet("Stock:Task:VIPCode",CreateTask资金流向)
for k in range(psutil.cpu_count(True)):
        r.DictSave("Stock:Task:ZJLX:Status","Task%s"%k,0)
print("资金流向任务创建完毕") 