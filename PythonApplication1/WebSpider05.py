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
from ChromeSpider import ChromeSpider

spider = ChromeSpider()
timeTag = time.strftime("%Y-%m-%d", time.localtime())
#检测文件夹的存在
path = "gupiao"
if False == os.path.exists(path) :
    os.mkdir(path)
path = "%s/%s" % (path,timeTag)
if False == os.path.exists(path) :
    os.mkdir(path)

url = "http://data.eastmoney.com/zjlx/detail.html"
chrome = webdriver.Chrome()
chrome.get(url)  
linkBtn = chrome.find_element_by_link_text("下一页")
clsVal = linkBtn.get_attribute('class')
pageIndex = 0
while clsVal != "nolink":
    #fs=open("%s/实时资金流向排行-%s-%s.txt"%(path,timeTag,pageIndex),"w",encoding="utf-8")
    #fs.write(chrome.page_source)
    #fs.close()


    detailArr = chrome.find_element_by_id("dt_1").find_elements_by_link_text("详情")
    
    
    detailLength = len(detailArr)
    index = 0
    #while index < detailLength:
    #    detail = detailArr[index]
    #    href = detail.get_attribute('href')
    #    print("%s" % href)
    #    isValidHref = re.match(r'^http://data.eastmoney.com/zjlx/\d{6}.html$', href)
    #    if isValidHref:    
    #        data = spider.LoadWeb(href).GetDataFromWeb()
    #        print(data)
    #        time.sleep(random.uniform(1,2))
    #    index+=1


    dataArr = chrome.find_element_by_id("dt_1").find_elements_by_link_text("数据")
    dataLength = len(dataArr)
    index = 0
    while index < dataLength:
        data = dataArr[index]
        href = data.get_attribute('href')
        print("%s" % href) 
        isValidHref = re.match(r'^http://data.eastmoney.com/stockdata/\d{6}.html$', href)
        if isValidHref:    
            data = spider.LoadWeb(href).GetDataFromWeb()
            print(data)

            #chrome.execute_script("arguments[0].scrollIntoView(false);",data)
            #time.sleep(random.uniform(1,2))
            #data=chrome.find_element_by_id("dt_1").find_elements_by_link_text("数据")[index]
            #data.click()
            #chrome.switch_to_window(chrome.window_handles[1])
            #fs=open("%s/%s-%s.txt"%(path,chrome.title.replace("*","@"),timeTag),"w",encoding="utf-8")
            #fs.write(chrome.page_source)
            #fs.close()
            #print(chrome.title.replace("*","@"))
            #chrome.close();
            #chrome.switch_to_window(chrome.window_handles[0])
            #print(chrome.title.replace("*","@"))
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