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
 
def SaveData融资融券ToRedis(code):
    jsonStr = HtmlConvertor.GetInst().LoadFromString(html=chrome.page_source).ConvertToJson() 
    jsonData=json.loads(jsonStr)
    if ("Tables" in jsonData and []!=jsonData["Tables"]): 
        tables = jsonData["Tables"]
        rows = tables[len(tables)-1]["body"]
        for row in rows:
            if 15==len(row):
                交易日期Tag = CONVERT.DateToInt(row[0])
                item={"Code":code
                      ,"交易日期":row[0]
                      ,"交易日期Tag":交易日期Tag
                      ,"收盘价":CONVERT.StrToFloat(row[1])
                      ,"涨跌幅":CONVERT.StrToFloat(row[2])
                      ,"融资余额":CONVERT.UnitStrToFloat(row[3])
                      ,"融资余额占流通市值比":CONVERT.UnitStrToFloat(row[4])
                      ,"融资买入额":CONVERT.UnitStrToFloat(row[5])
                      ,"融资偿还额":CONVERT.UnitStrToFloat(row[6])
                      ,"融资净买入":CONVERT.UnitStrToFloat(row[7])
                      ,"融券余额":CONVERT.UnitStrToFloat(row[8])
                      ,"融券余量":CONVERT.UnitStrToFloat(row[9])
                      ,"融券卖出量":CONVERT.UnitStrToFloat(row[10])
                      ,"融券偿还量":CONVERT.UnitStrToFloat(row[11])
                      ,"融券净卖出":CONVERT.UnitStrToFloat(row[12])
                      ,"融资融券余额":CONVERT.UnitStrToFloat(row[13])
                      ,"融资融券余额":CONVERT.UnitStrToFloat(row[14])
                      }
                print(item)
                qName融资融券="Stock:RZRQ:%s"%code
                r.SortDictSave(qName融资融券,item,交易日期Tag)

 
def ProcTask融资融券(qName,qItem):
    qItem = json.loads(qItem)
    code=qItem["Code"]
    url=qItem["Url"]#北向持股明细列表
    retryCount=qItem["RetryCount"]
    try:
        chrome.get(url)  
        time.sleep(random.uniform(2,4))
        SaveData融资融券ToRedis(code)
        print("已保存 %s %s"%(code,url))
    except BaseException as e:
        retryCount=retryCount-1
        if 0<retryCount:
            task={"Code":code,"Url":url,"RetryCount":retryCount}
            r.QueueEn("Stock:Task:RZRQ",json.dumps(task,ensure_ascii=False))
        print("%s 异常 %s %s",(qName,url,e))
        time.sleep(60)
    pass

def CreateTask融资融券(dictName,code):
    url = "http://data.eastmoney.com/rzrq/detail/%s.html"%code 
    task={"Code":code,"Url":url,"RetryCount":3}
    qName="Stock:Task:RZRQ"
    r.QueueEn(qName,json.dumps(task,ensure_ascii=False))
    pass
 
r.TraverseDict("Stock:BaseData:AllCode",CreateTask融资融券)
print("列表任务创建完毕")
time.sleep(10)
r.ProcQueue("Stock:Task:RZRQ",ProcTask融资融券)
print("OK") 
chrome.Quit()