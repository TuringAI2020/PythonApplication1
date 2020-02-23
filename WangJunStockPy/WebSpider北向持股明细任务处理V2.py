import os
import random
import time
import sys
import gzip
import urllib
import urllib.request
import io  #StringIO模块就是在内存中读写str
import re
import json
import datetime

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from ChromeSpider import ChromeSpider
from CHECKER import CHECKER
from HtmlConvertor import HtmlConvertor
from RClient import RClient
from CONVERTOR import CONVERT
import SyncNotice

r=RClient.GetInst()
 
spider = ChromeSpider() 
 
def 北向持股明细任务处理(qName,qItem): 
     task = json.loads(qItem)
     code=task["Code"]
     url=task["Url"]
     retryCount=task["RetryCount"] 
     taskID=qName.split(":")[3]
     try:
         jsonStr = spider.LoadWeb(url,"北向持股明细").GetDataFromWeb()
         jsonData=json.loads(jsonStr)
         if "Tables" in jsonData: 
            tables = jsonData["Tables"]
            if 0<len(tables):
                rows=tables[len(tables)-1]["body"]
                for row in rows:
                    if 12 == len(row): 
                        持股日期Tag=CONVERT.DateToInt(row[0])
                        item={
                            "Code":code
                              ,"持股日期":row[0]
                              ,"持股日期Tag":持股日期Tag
                              ,"股票代码":row[1]
                              ,"股票简称":row[2]
                              ,"当日收盘价":CONVERT.StrToFloat(row[3])
                              ,"当日涨跌幅":CONVERT.StrToFloat(row[4])
                              ,"机构名称":row[5]
                              ,"持股数量":CONVERT.UnitStrToFloat(row[6])
                              ,"持股市值":CONVERT.UnitStrToFloat(row[7])
                              ,"持股数量占A股百分比":CONVERT.StrToFloat(row[8])
                              ,"持股市值变化1日":CONVERT.UnitStrToFloat(row[9])
                              ,"持股市值变化5日":CONVERT.UnitStrToFloat(row[10])
                              ,"持股市值变化10日":CONVERT.UnitStrToFloat(row[11])
                              }
                        qName北向持股="Stock:BXCGMX:%s"%code
                        targetNameSpace=qName北向持股
                        r.SortDictSave(qName北向持股,item,持股日期Tag)
                        SyncNotice.SendSyncNotice(targetNameSpace,{"namespace":targetNameSpace,"code":code,"score":持股日期Tag,"value":item,"type":"SortedSet"})
                r.DictSave("Stock:Task:BXCGMX:Status","%s"%taskID,{"StartTime": startTime.strftime('%Y-%m-%d %H:%M:%S'),"UpdateTime":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"Running":(datetime.datetime.now()-startTime).seconds})
                print("%s %s"%(taskID,item))
     except BaseException as e:
        retryCount=retryCount-1
        if 0<retryCount:
            task={"Code":code,"Url":url,"RetryCount":retryCount}
            r.QueueEn(qName,json.dumps(task,ensure_ascii=False))
        print("%s %s"%(qItem,e))
        time.sleep(120)
     pass
 
taskID="0"
startTime =   datetime.datetime.now()

def 任务占有(dictName,key,val,pageIndex,pageCount,pageSize,curIndex,total):
    if val==0 or "0" == val:
        taskID=key
        r.DictSave("Stock:Task:BXCGMX:Status","%s"%taskID,{"StartTime": startTime.strftime('%Y-%m-%d %H:%M:%S'),"UpdateTime":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"Running":(datetime.datetime.now()-startTime).seconds})
        r.ProcQueue("Stock:Task:BXCGMX:%s"%taskID,北向持股明细任务处理)
    pass


#oldKeys= r.QueryKeys("Stock:北向持股:*");
#for oldKey in oldKeys[1]:
#    newKey = oldKey.replace("北向持股","BXCGMX")
#    r.RenameKeyNX(oldKey,newKey)
#    print("%s %s"%(oldKey,newKey))
r.DeleteKeys("Stock:北向持股:*")

r.TraverseDict("Stock:Task:BXCGMX:Status",任务占有) 
print("OK") 
spider.Quit()