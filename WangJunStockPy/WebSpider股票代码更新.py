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
 
def DownloadAllCode(): 
    url = "http://quote.eastmoney.com/center/gridlist.html#hs_a_board"#沪深A股

    chrome.get(url)  
    linkBtn = chrome.find_element_by_link_text("下一页")
    clsVal = linkBtn.get_attribute('class')
    pageIndex = 0
    while clsVal != "disabled": 
        chrome.switch_to_window(chrome.window_handles[0]) 
        linkBtn = chrome.find_element_by_link_text("下一页")
        chrome.execute_script("arguments[0].scrollIntoView(false);",linkBtn)
        clsVal = linkBtn.get_attribute('class')

        jsonStr = HtmlConvertor.GetInst().LoadFromString(html=chrome.page_source).ConvertToJson() 
        jsonData=json.loads(jsonStr)
        if ("Tables" in jsonData and []!=jsonData["Tables"]):
            rows = jsonData["Tables"][0]["body"]
            for row in rows:
                code=row[1]
                name=row[2]
                if (6 == len(code) and 0<len(name)):
                    RClient.GetInst().DictSave("Stock:BaseData:AllCode",code,name.replace("*","@"))
                    print("%s %s"%(code,name))
            print("页码 %d"%pageIndex) 
        else:
            print("%d 页数据未能加载"%pageIndex)
            time.sleep(20)
            pass
        pageIndex+=1
        linkBtn.click()
        time.sleep(random.uniform(2,4))
    chrome.quit()
     
DownloadAllCode() 
print("OK")