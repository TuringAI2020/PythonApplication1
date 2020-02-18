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

r=RClient.GetInst()

def CreateEmptyItem(table):
    rows = table["body"]
    item = {}
    for row in rows:
         item[row[0].strip()] = ""
    return item

def CreateEmptyItemList(table):
    rows = table["body"]
    itemCount = 0
    arr = []
    if(0 < len(rows)):
        itemCount = len(rows[0]) - 1
    while 0 < itemCount:
        item = CreateEmptyItem(table)
        arr.append(item)
        itemCount-=1
    return arr

def FillItemList(table):
     arr = CreateEmptyItemList(table)
     rows = table["body"]
     
     for row in rows:
         key = row[0]
         rowIndex = 1
         while rowIndex < len(arr):
             if True != CHECKER.IsDate(row[rowIndex]): 
                arr[rowIndex - 1][key] = CONVERT.UnitStrToFloat(row[rowIndex],unit=None)
             else:
                 if 8 == len(row[rowIndex]):
                     row[rowIndex] = "20" + row[rowIndex] 
                 arr[rowIndex - 1][key + "Tag"] = CONVERT.DateToInt(row[rowIndex])
                 arr[rowIndex - 1][key] = row[rowIndex] 
                 arr[rowIndex - 1]["DateTag"] = CONVERT.DateToInt(row[rowIndex])
                
             rowIndex+=1
     return arr  

spider = ChromeSpider()

startTime =   datetime.datetime.now()


def ProcTask新财务分析(qName,qItem): 
    qItem = json.loads(qItem)
    code=qItem["Code"]
    url=qItem["Url"]#北向持股明细列表
    retryCount=qItem["RetryCount"]
    taskID=qName.split(":")[3] 
 
    try:
        jsonStr = spider.LoadWeb(url,"新财务分析").GetDataFromWeb()
        jsonData=json.loads(jsonStr)
        财务主要指标 = jsonData["Tables"][0]
        财务主要指标 = FillItemList(财务主要指标)
        财务主要指标 = list(filter(lambda x:"每股指标Tag" in x,财务主要指标))
        for item in  财务主要指标:
            item["Code"]=code
            dateTag = item["每股指标Tag"]
            r.DictSave("Stock:Detail:%s"%code,"财务主要指标:%s"%dateTag,item)
        r.DictSave("Stock:Task:CWFX:Status","%s"%taskID,{"Running(分钟)":(datetime.datetime.now()-startTime).seconds/60,"StartTime": startTime.strftime('%Y-%m-%d %H:%M:%S'),"UpdateTime":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
    except BaseException as e:
        retryCount=retryCount-1
        if 0<retryCount:
            task={"Code":code,"Url":url,"RetryCount":retryCount}
            r.QueueEn(qName,json.dumps(task,ensure_ascii=False))
        print("%s 异常 %s %s",(qName,url,e))
        time.sleep(120)  

def 任务占有(dictName,key,val,pageIndex,pageCount,pageSize,curIndex,total):
    if val==0 or "0" == val:
        taskID=key
        print("新财务分析任务处理启动 %s"%taskID)
        r.DictSave("Stock:Task:CWFX:Status","%s"%taskID,{"Running(分钟)":(datetime.datetime.now()-startTime).seconds/60,"StartTime": startTime.strftime('%Y-%m-%d %H:%M:%S'),"UpdateTime":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
        r.ProcQueue("Stock:Task:CWFX:%s"%taskID,ProcTask新财务分析)
    pass
r.TraverseDict("Stock:Task:CWFX:Status",任务占有)
spider.Quit()