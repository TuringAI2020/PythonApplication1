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
from CHECKER import CHECKER
from Config import Cfg
import requests
from HtmlConvertor import HtmlConvertor 
from CONVERTOR import CONVERT

  

chrome_opt = Options()      # 创建参数设置对象.
chrome_opt.add_argument('--headless')   # 无界面化.
chrome_opt.add_argument('--disable-gpu')    # 配合上面的无界面化.
chrome_opt.add_argument('--window-size=1920,1080')   # 设置窗口大小, 窗口大小会有影响.
chrome = webdriver.Chrome( chrome_options=chrome_opt) 
timeTag = time.strftime("%Y-%m-%d", time.localtime())
 
def DownloadAllCode(): 
    #serverUrl="http://122.51.159.248:5000/YunStock2Service?keyName=GJDCGGGMX&taskId=%s" % taskId
    serverUrl = "http://127.0.0.1:5000/YunStock2Service?keyName=GJDCGGGMX&taskId=%s" % taskId


    url = "http://data.eastmoney.com/gjdcg/mingxi.aspx?date=2020-03-31"#沪深A股

    chrome.get(url)  
    linkBtn = chrome.find_element_by_link_text("下一页")
    clsVal = linkBtn.get_attribute('class')
    pageIndex = 0
    while True != CHECKER.Contains(clsVal,"nolink"): 
        chrome.switch_to_window(chrome.window_handles[0]) 
        linkBtn = chrome.find_element_by_link_text("下一页")
        chrome.execute_script("arguments[0].scrollIntoView(false);",linkBtn)
        clsVal = linkBtn.get_attribute('class')

        jsonStr = HtmlConvertor.GetInst().LoadFromString(html=chrome.page_source).ConvertToJson() 
        jsonData=json.loads(jsonStr)
        if ("Tables" in jsonData and []!=jsonData["Tables"]):
            tables = jsonData["Tables"]
            rows = tables[len(tables) - 1]["body"]
            postArr=[]
            for row in rows: 
                if (11 == len(row)):
                    item={
                        "Code":row[1],
                        "股票简称":row[2],
                        "持股数量合计":CONVERT.UnitStrToFloat(row[4]),
                        "持股数量变动":CONVERT.UnitStrToFloat(row[5]),
                        "持股市值合计":CONVERT.UnitStrToFloat(row[6]),
                        "持股市值变动":CONVERT.UnitStrToFloat(row[7]),
                        "持股比例合计":CONVERT.StrToFloat(row[8]),
                        "持股比例变动":CONVERT.StrToFloat(row[9]),
                        "公告日期":row[10],
                        "公告日期Tag":CONVERT.DateToInt(row[10]),
                        }
                    postArr.append(item) 
            post_data={"keyName":"GJDCGGGMX",  "jsonReq": json.dumps({},ensure_ascii=False),"jsonRes": json.dumps(postArr,ensure_ascii=False)}
            res2 = requests.post(serverUrl,data=post_data)
            print("POST %s \r\n RES %s \r\n --------- \r\n"%(post_data,res2.text))
        else:
            print("%d 页数据未能加载"%pageIndex)
            time.sleep(20)
            pass
        pageIndex+=1 
        linkBtn = chrome.find_element_by_link_text("下一页")
        linkBtn.click()
        time.sleep(random.uniform(3,5))
    chrome.quit()
     
DownloadAllCode()