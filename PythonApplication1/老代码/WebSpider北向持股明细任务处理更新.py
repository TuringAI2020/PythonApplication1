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
 
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from ChromeSpider import ChromeSpider
from CHECKER import CHECKER
from HtmlConvertor import HtmlConvertor
from RClient import RClient
from CONVERTOR import CONVERT

r=RClient.GetInst()
 
spider = ChromeSpider()
timeTag = time.strftime("%Y-%m-%d", time.localtime())
 
def 北向持股明细任务处理(qName,qItem): 
     task = json.loads(qItem)
     code=task["Code"]
     url=task["Url"]
     retryCount=task["RetryCount"] 
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
                        qName北向持股="Stock:北向持股:%s"%code
                        r.SortDictSave(qName北向持股,item,持股日期Tag)
                        print(item)
     except BaseException as e:
        retryCount=retryCount-1
        if 0<retryCount:
            task={"Code":code,"Url":url,"RetryCount":retryCount}
            r.QueueEn(qName,json.dumps(task,ensure_ascii=False))
        print("%s %s"%(qItem,e))
        time.sleep(60)
     pass
 
r.ProcQueue("Stock:Task:北向持股明细任务",北向持股明细任务处理)
print("OK") 
spider.Quit()