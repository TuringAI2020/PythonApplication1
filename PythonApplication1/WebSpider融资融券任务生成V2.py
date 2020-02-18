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
def CreateTask融资融券(dictName,key,val,pageIndex,pageCount,pageSize,curIndex,total):
    code=key
    threadCount=psutil.cpu_count(True)
    taskID=CONVERT.StrToInt(code[len(code)-1])%threadCount
    url = "http://data.eastmoney.com/rzrq/detail/%s.html"%code 
    task={"Code":code,"Url":url,"RetryCount":3}
    qName="Stock:Task:RZRQ:Task%d"%taskID
    r.QueueEn(qName,json.dumps(task,ensure_ascii=False))
    print("CreateTask融资融券 %s"%code)
    pass

print("WebSpider融资融券任务生成V2")
r.DeleteKeys("Stock:Task:RZRQ:*")
r.TraverseDict("Stock:BaseData:AllCode",CreateTask融资融券)
for k in range(psutil.cpu_count(True)):
        r.DictSave("Stock:Task:RZRQ:Status","Task%s"%k,0)
print("融资融券任务创建完毕") 