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
import psutil

 
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options 
from CHECKER import CHECKER
from HtmlConvertor import HtmlConvertor
from RClient import RClient
from CONVERTOR import CONVERT

r=RClient.GetInst()

chrome_opt = Options()      # 创建参数设置对象.
chrome_opt.add_argument('--headless')   # 无界面化.
chrome_opt.add_argument('--disable-gpu')    # 配合上面的无界面化.
chrome_opt.add_argument('--window-size=400,400')   # 设置窗口大小, 窗口大小会有影响.
chrome = webdriver.Chrome( chrome_options=chrome_opt)
chrome.implicitly_wait(10) 
timeTag = time.strftime("%Y-%m-%d", time.localtime())
 
def SaveTask北向持股明细ToRedis(code):
    jsonStr = HtmlConvertor.GetInst().LoadFromString(html=chrome.page_source).ConvertToJson() 
    jsonData=json.loads(jsonStr)
    if ("Links" in jsonData and []!=jsonData["Links"]): 
        links = jsonData["Links"]
        links = list(filter(lambda x:x["Text"]=="更多",links))
        for link in links:
            text  = link["Text"].strip()
            href  = link["Href"].strip()
            if "更多" == text and CHECKER.StartWith(href,"^\/hsgtcg\/StockInstitutionDetail.aspx\?stock="):
                href="http://data.eastmoney.com/%s"%href
                task={"Code":code,"Url":href,"RetryCount":3}
                taskGroupID = int(code[len(code)-1])%4
                qName="Stock:Task:BXCGMX:Task%d"%taskGroupID
                r.QueueEn(qName,json.dumps(task,ensure_ascii=False))
                print(href)

def CreateTask北向持股明细(qName,qItem):
    qItem = json.loads(qItem)
    code=qItem["Code"]
    url=qItem["Url"]#北向持股明细列表
    retryCount=qItem["RetryCount"]
    try:
        chrome.get(url)  
        time.sleep(random.uniform(2,4))
        if True != CHECKER.Contains(chrome.page_source,"下一页"):
            SaveTask北向持股明细ToRedis(code)
            print("生成 单页任务 %s %s"%(code,url))
        else:
            linkBtn = chrome.find_element_by_link_text("下一页") 
            clsVal = linkBtn.get_attribute('class')
            pageIndex = 0
            while False == CHECKER.Contains(clsVal,"nolink"):  
                chrome.switch_to_window(chrome.window_handles[0]) 
                linkBtn = chrome.find_element_by_link_text("下一页")
                chrome.execute_script("arguments[0].scrollIntoView(false);",linkBtn)
                clsVal = linkBtn.get_attribute('class')
                SaveTask北向持股明细ToRedis(code)
                print("生成 多页任务 %s %s"%(code,url))
                pageIndex+=1
                linkBtn.click()
                time.sleep(random.uniform(2,4))
    except BaseException as e:
        retryCount=retryCount-1
        if 0<retryCount:
            task={"Code":code,"Url":url,"RetryCount":retryCount}
            r.QueueEn("Stock:Task:北向持股明细列表任务",json.dumps(task,ensure_ascii=False))
        print("%s 异常 %s %s"%(qName,url,e))
        time.sleep(120)
    pass

def CreateTask北向持股明细列表(dictName,key,val,pageIndex,pageCount,pageSize,curIndex,total):
    code=key
    url = "http://data.eastmoney.com/hsgtcg/StockHdDetail.aspx?stock=%s"%code #北向持股明细列表
    task={"Code":code,"Url":url,"RetryCount":3}
    qName="Stock:Task:北向持股明细列表任务"
    r.QueueEn(qName,json.dumps(task,ensure_ascii=False))
    pass

r.DeleteKeys("Stock:Task:北向持股明细列表任务")
r.DeleteKeys("Stock:Task:BXCGMX:*")
r.TraverseDict("Stock:BaseData:AllCode",CreateTask北向持股明细列表)
for k in range(psutil.cpu_count(True)):
    r.DictSave("Stock:Task:BXCGMX:Status","Task%s"%k,0)
print("北向持股明细任务创建完毕")

r.ProcQueue("Stock:Task:北向持股明细列表任务",CreateTask北向持股明细)
print("OK")
chrome.quit() 