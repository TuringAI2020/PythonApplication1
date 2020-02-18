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

def callback(input,args):
     output = input
     title = input["Title"]
     if True == CHECKER.HasHanZi(title):
         dateTag = time.strftime("%Y%m%d", time.localtime())
         output["Name"] =  args["Name"]
         output["Code"] =  args["Code"]
         output["DateTag"] = dateTag
         output["PageTag"] = args["PageTag"]
         return output
     else:
         qName="FailDownload"
         RClient.GetInst().QueueEn(qName,args)
         return None

         pass

chrome_opt = Options()      # 创建参数设置对象.
chrome_opt.add_argument('--headless')   # 无界面化.
chrome_opt.add_argument('--disable-gpu')    # 配合上面的无界面化.
chrome_opt.add_argument('--window-size=400,1080')   # 设置窗口大小, 窗口大小会有影响.
chrome = webdriver.Chrome( chrome_options=chrome_opt)
spider = ChromeSpider()
timeTag = time.strftime("%Y-%m-%d", time.localtime())
 
def CreateTask(dictName,code):
    code2="SH"+code if code[0]=="6" else "SZ"+code
    url = "http://f10.eastmoney.com/f10_v2/FinanceAnalysis.aspx?code=%s"%code2 #核心题材
    task={"Code":code,"Url":url,"RetryCount":3}
    qName="Stock:Task:新财务分析更新"
    r.QueueEn(qName,json.dumps(task,ensure_ascii=False))
    print("生成任务 %s"%url)
    pass

def 新财务分析数据更新回调函数(): 
    #code2="SH"+code if code[0]=="6" else "SZ"+code
    #url = "http://f10.eastmoney.com/f10_v2/FinanceAnalysis.aspx?code=%s"%code2 #核心题材
    qName="Stock:Task:新财务分析更新"
    task = r.QueueDe("Stock:Task:新财务分析更新")
    while None!=task:
        try:
            task = json.loads(task)
            code=task["Code"]
            url=task["Url"]
            retryCount=task["RetryCount"]
            jsonStr = spider.LoadWeb(url,"新财务分析").GetDataFromWeb()
            jsonData=json.loads(jsonStr)
            财务主要指标 = jsonData["Tables"][0]
            财务主要指标 = FillItemList(财务主要指标)
            财务主要指标 = list(filter(lambda x:"每股指标Tag" in x,财务主要指标))
            for item in  财务主要指标:
                item["Code"]=code
                dateTag = item["每股指标Tag"]
                r.DictSave("Stock:Detail:%s"%code,"财务主要指标:%s"%dateTag,item)
            print("%s 剩余 %d "%(qName,r.Count(qName)))
        except BaseException as e:
            retryCount=retryCount-1
            if 0<retryCount:
                task={"Code":code,"Url":url,"RetryCount":retryCount}
                r.QueueEn(qName,json.dumps(task,ensure_ascii=False))
            print("%s 异常 %s %s",(qName,url,e))
            time.sleep(60)
        finally:
            task = r.QueueDe(qName)
      
r.TraverseDict("Stock:BaseData:AllCode",CreateTask)
新财务分析数据更新回调函数()
print("OK")
chrome.quit()
spider.Quit()