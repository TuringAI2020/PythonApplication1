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
#from ChromeSpider import ChromeSpider
from CHECKER import CHECKER
from HtmlConvertor import HtmlConvertor
from RClient import RClient
from CONVERTOR import CONVERT
import SyncNotice

r=RClient.GetInst()

chrome_opt = Options()      # 创建参数设置对象.
chrome_opt.add_argument('--headless')   # 无界面化.
chrome_opt.add_argument('--disable-gpu')    # 配合上面的无界面化.
chrome_opt.add_argument('--window-size=400,1080')   # 设置窗口大小, 窗口大小会有影响.
chrome = webdriver.Chrome( chrome_options=chrome_opt)
chrome.implicitly_wait(10)

 
def SaveData北向成交明细ToRedis(code):
    jsonStr = HtmlConvertor.GetInst().LoadFromString(html=chrome.page_source).ConvertToJson() 
    jsonData=json.loads(jsonStr)
    if ("Tables" in jsonData and []!=jsonData["Tables"]): 
        tables = jsonData["Tables"]
        rows = tables[len(tables)-1]["body"]
        for row in rows:
            if 9==len(row):
                日期Tag = CONVERT.DateToInt(row[0])
                item={"Code":code
                      ,"日期":row[0]
                      ,"日期Tag":CONVERT.DateToInt(row[0])
                      ,"当日排名":CONVERT.StrToInt(row[2])
                      ,"收盘价":CONVERT.StrToFloat(row[3])
                      ,"涨跌幅":CONVERT.UnitStrToFloat(row[4])
                      ,"沪深股通净买额":CONVERT.UnitStrToFloat(row[5])
                      ,"沪深股通买入金额":CONVERT.UnitStrToFloat(row[6])
                      ,"沪深股通卖出金额":CONVERT.UnitStrToFloat(row[7])
                      ,"沪深股通成交金额":CONVERT.UnitStrToFloat(row[8])}
                print("北向成交明细 Task%s %s"%(taskID,item))
                qName北向成交="Stock:BXCJMX:%s"%code
                targetNameSpace=qName北向成交
                r.SortDictSave(qName北向成交,item,日期Tag)
                SyncNotice.SendSyncNotice(targetNameSpace,{"namespace":targetNameSpace,"code":code,"score":日期Tag,"value":item,"type":"SortedSet"})
 
def ProcTask北向成交明细(qName,qItem):
    qItem = json.loads(qItem)
    code=qItem["Code"]
    url=qItem["Url"]#北向持股明细列表
    retryCount=qItem["RetryCount"]
    try:
        chrome.get(url)  
        time.sleep(random.uniform(2,3))
        SaveData北向成交明细ToRedis(code)
        taskID=qName.split(":")[3]
        r.DictSave("Stock:Task:BXCJMX:Status","%s"%taskID,{"StartTime": startTime.strftime('%Y-%m-%d %H:%M:%S'),"UpdateTime":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"Running":(datetime.datetime.now()-startTime).seconds})
        print("已保存 %s %s %s"%(taskID,code,url))

    except BaseException as e:
        retryCount=retryCount-1
        if 0<retryCount:
            task={"Code":code,"Url":url,"RetryCount":retryCount}
            r.QueueEn(qName,json.dumps(task,ensure_ascii=False))
        print("%s 异常 %s %s",(qName,url,e))
        time.sleep(60)
    pass
 
taskID="0"
startTime =   datetime.datetime.now()
def 任务占有(dictName,key,val,pageIndex,pageCount,pageSize,curIndex,total):
    if val==0 or "0" == val:
        taskID=key
        r.DictSave("Stock:Task:BXCJMX:Status","%s"%taskID,{"StartTime": startTime.strftime('%Y-%m-%d %H:%M:%S'),"UpdateTime":datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"Running":(datetime.datetime.now()-startTime).seconds})
        r.ProcQueue("Stock:Task:BXCJMX:%s"%taskID,ProcTask北向成交明细)
    pass

r.TraverseDict("Stock:Task:BXCJMX:Status",任务占有)
print("北向成交明细运行完毕 Task%s"%taskID) 
chrome.quit() 