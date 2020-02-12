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

chrome_opt = Options()      # 创建参数设置对象.
chrome_opt.add_argument('--headless')   # 无界面化.
chrome_opt.add_argument('--disable-gpu')    # 配合上面的无界面化.
chrome_opt.add_argument('--window-size=400,1080')   # 设置窗口大小, 窗口大小会有影响.
chrome = webdriver.Chrome( chrome_options=chrome_opt)
chrome.implicitly_wait(10)
#spider = ChromeSpider()
timeTag = time.strftime("%Y-%m-%d", time.localtime())
 
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
                print(item)
                qName北向成交="Stock:BXCJMX:%s"%code
                r.SortDictSave(qName北向成交,item,日期Tag)

 
def ProcTask北向成交明细(qName,qItem):
    qItem = json.loads(qItem)
    code=qItem["Code"]
    url=qItem["Url"]#北向持股明细列表
    retryCount=qItem["RetryCount"]
    try:
        chrome.get(url)  
        time.sleep(random.uniform(2,4))
        SaveData北向成交明细ToRedis(code)
        print("已保存 %s %s"%(code,url))
    except BaseException as e:
        retryCount=retryCount-1
        if 0<retryCount:
            task={"Code":code,"Url":url,"RetryCount":retryCount}
            r.QueueEn("Stock:Task:BXCJMX",json.dumps(task,ensure_ascii=False))
        print("%s 异常 %s %s",(qName,url,e))
        time.sleep(60)
    pass

def CreateTask北向成交明细(dictName,code):
    url = "http://data.eastmoney.com/hsgt/%s.html"%code #北向持股明细列表
    task={"Code":code,"Url":url,"RetryCount":3}
    qName="Stock:Task:BXCJMX"#北向成交明细
    r.QueueEn(qName,json.dumps(task,ensure_ascii=False))
    pass
 
r.TraverseDict("Stock:BaseData:AllCode",CreateTask北向成交明细)
print("列表任务创建完毕")
time.sleep(10)
r.ProcQueue("Stock:Task:BXCJMX",ProcTask北向成交明细)
print("OK")
chrome.quit()
#spider.Quit()