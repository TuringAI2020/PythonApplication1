import os
import random
import time
import sys
import gzip
import urllib
import urllib.request
import io  #StringIO模块就是在内存中读写str
import re


# 1.  导入Python SSL处理模块
import ssl
import jieba

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from ChromeSpider import ChromeSpider
from CHECKER import CHECKER
from RClient import RClient

def callback(input):
     output = input
     title = input["Title"]
     if True == CHECKER.HasHanZi(title):
         name = title.split('(')[0]
         code = title.split('(')[1].split(')')[0]
         dateTag = time.strftime("%Y%m%d", time.localtime())
         pageTag = title.split('(')[1].split(')')[1].split(" ")[0].strip()
         output["Name"] = name
         output["Code"] = code
         output["DateTag"] = dateTag
         output["PageTag"] = pageTag
         return output
     else:
         qName="FailDownload"
         RClient.GetInst().QueueEn(qName,input)
         return None

         pass

chrome_opt = Options()      # 创建参数设置对象.
chrome_opt.add_argument('--headless')   # 无界面化.
chrome_opt.add_argument('--disable-gpu')    # 配合上面的无界面化.
chrome_opt.add_argument('--window-size=400,1080')   # 设置窗口大小, 窗口大小会有影响.
chrome = webdriver.Chrome( chrome_options=chrome_opt)
spider = ChromeSpider()
timeTag = time.strftime("%Y-%m-%d", time.localtime())
 

url = "http://data.eastmoney.com/zjlx/detail.html"

chrome.get(url)  
linkBtn = chrome.find_element_by_link_text("下一页")
clsVal = linkBtn.get_attribute('class')
pageIndex = 0
while clsVal != "nolink": 

    detailArr = chrome.find_element_by_id("dt_1").find_elements_by_link_text("详情")
     
    detailLength = len(detailArr)
    index = 0
    while index < detailLength:
        detail = detailArr[index]
        href = detail.get_attribute('href')
        print("%s" % href)
        isValidHref = re.match(r'^http://data.eastmoney.com/zjlx/\d{6}.html$', href)
        if isValidHref:    
            spider.LoadWeb(href).SaveDataToRedis(callback) 
            #print(data)
            time.sleep(random.uniform(1,2))
        index+=1


    dataArr = chrome.find_element_by_id("dt_1").find_elements_by_link_text("数据")
    dataLength = len(dataArr)
    index = 0
    while index < dataLength:
        data = dataArr[index]
        href = data.get_attribute('href')
        print("%s" % href) 
        isValidHref = re.match(r'^http://data.eastmoney.com/stockdata/\d{6}.html$', href)
        if isValidHref:    
            data = spider.LoadWeb(href).SaveDataToRedis(callback) 
            print(data) 
            time.sleep(random.uniform(1,2))
        index+=1

    chrome.switch_to_window(chrome.window_handles[0]) 
    linkBtn = chrome.find_element_by_link_text("下一页")
    chrome.execute_script("arguments[0].scrollIntoView(false);",linkBtn)
    clsVal = linkBtn.get_attribute('class')
    linkBtn.click()
    pageIndex+=1
    print(pageIndex)

    time.sleep(random.uniform(10,20))
print("OK")