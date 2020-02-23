import os
import random
import time
import sys 
import io  #StringIO模块就是在内存中读写str
import re
import json  
from RClient import RClient
from CONVERTOR import CONVERT
import psutil
r=RClient.GetInst()
 

def CreateTask北向成交明细(setName,item):
    code=item[0]
    url = "http://data.eastmoney.com/hsgt/%s.html"%code #北向持股明细列表
    task={"Code":code,"Url":url,"RetryCount":3}
    taskID=CONVERT.StrToInt(code[len(code)-1])%psutil.cpu_count(True)
    qName="Stock:Task:BXCJMX:Task%s"%taskID
    r.QueueEn(qName,json.dumps(task,ensure_ascii=False)) 
    pass
r.DeleteKeys("Stock:Task:BXCJMX:*")
r.TraverseSortedSet("Stock:Task:VIPCode",CreateTask北向成交明细)
for k in range(psutil.cpu_count(True)):
        r.DictSave("Stock:Task:BXCJMX:Status","Task%s"%k,0)
print("WebSpider北向成交明细任务生成V2")
time.sleep(10) 
print("OK") 