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
#from ChromeSpider import ChromeSpider
from CHECKER import CHECKER
from HtmlConvertor import HtmlConvertor
from RClient import RClient
from CONVERTOR import CONVERT

r=RClient.GetInst()

chrome_opt = Options()      # 创建参数设置对象.
chrome_opt.add_argument('--headless')   # 无界面化.
chrome_opt.add_argument('--disable-gpu')    # 配合上面的无界面化.
chrome_opt.add_argument('--window-size=400,1080')   # 设置窗口大小, 窗口大小会有影响.
chrome = webdriver.Chrome( chrome_options=chrome_opt)
chrome.implicitly_wait(10) 
timeTag = time.strftime("%Y-%m-%d", time.localtime())
 
def SaveData资金流向ToRedis(code):
    jsonStr = HtmlConvertor.GetInst().LoadFromString(html=chrome.page_source).ConvertToJson() 
    jsonData=json.loads(jsonStr)
    if ("Tables" in jsonData and []!=jsonData["Tables"]): 
        tables = jsonData["Tables"]
        rows = tables[len(tables)-1]["body"]
        for row in rows:
            if 13==len(row):
                日期Tag = CONVERT.DateToInt(row[0])
                item={"Code":code
                      ,"日期":row[0]
                      ,"日期Tag":日期Tag
                      ,"收盘价":CONVERT.StrToFloat(row[1])
                      ,"涨跌幅":CONVERT.UnitStrToFloat(row[2])
                      ,"主力净流入净额":CONVERT.UnitStrToFloat(row[3])
                      ,"主力净流入净占比":CONVERT.UnitStrToFloat(row[4])
                      ,"超大单净流入净额":CONVERT.UnitStrToFloat(row[5])
                      ,"超大单净流入净占比":CONVERT.UnitStrToFloat(row[6])
                      ,"大单净流入净额":CONVERT.UnitStrToFloat(row[7])
                      ,"大单净流入净占比":CONVERT.UnitStrToFloat(row[8])
                      ,"中单净流入净额":CONVERT.UnitStrToFloat(row[9])
                      ,"中单净流入净占比":CONVERT.UnitStrToFloat(row[10])
                      ,"小单净流入净额":CONVERT.UnitStrToFloat(row[11])
                      ,"小单净流入净占比":CONVERT.UnitStrToFloat(row[12])
                      }
                print(item)
                qName资金流向="Stock:ZJLX:%s"%code
                r.SortDictSave(qName资金流向,item,日期Tag)

 
def ProcTask资金流向(qName,qItem):
    qItem = json.loads(qItem)
    code=qItem["Code"]
    url=qItem["Url"]#北向持股明细列表
    retryCount=qItem["RetryCount"]
    try:
        chrome.get(url)  
        time.sleep(random.uniform(2,4))
        SaveData资金流向ToRedis(code)
        print("已保存 %s %s"%(code,url))
    except BaseException as e:
        retryCount=retryCount-1
        if 0<retryCount:
            task={"Code":code,"Url":url,"RetryCount":retryCount}
            r.QueueEn("Stock:Task:ZJLX",json.dumps(task,ensure_ascii=False))
        print("%s 异常 %s %s",(qName,url,e))
        time.sleep(60)
    pass

def CreateTask资金流向(dictName,code):
    url = "http://data.eastmoney.com/zjlx/%s.html"%code 
    task={"Code":code,"Url":url,"RetryCount":3}
    qName="Stock:Task:ZJLX"
    r.QueueEn(qName,json.dumps(task,ensure_ascii=False))
    pass
 
r.TraverseDict("Stock:BaseData:AllCode",CreateTask资金流向)
print("列表任务创建完毕")
time.sleep(10)
r.ProcQueue("Stock:Task:ZJLX",ProcTask资金流向)
print("OK") 
chrome.Quit()