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
def CreateTask新财务分析(dictName,key,val,pageIndex,pageCount,pageSize,curIndex,total):
    code=key
    code2="SH"+code if code[0]=="6" else "SZ"+code
    url = "http://f10.eastmoney.com/f10_v2/FinanceAnalysis.aspx?code=%s"%code2 #核心题材
    threadCount=psutil.cpu_count(True)
    taskID=CONVERT.StrToInt(code[len(code)-1])%threadCount
    task={"Code":code,"Url":url,"RetryCount":3}
    qName="Stock:Task:CWFX:Task%d"%taskID
    r.QueueEn(qName,json.dumps(task,ensure_ascii=False))
    print("CreateTask新财务分析 %s"%code)
    pass

print("WebSpider新财务分析任务生成V2")
r.DeleteKeys("Stock:Task:CWFX:*")
r.TraverseDict("Stock:BaseData:AllCode",CreateTask新财务分析)
for k in range(psutil.cpu_count(True)):
        r.DictSave("Stock:Task:CWFX:Status","Task%s"%k,0)
print("新财务分析任务创建完毕") 