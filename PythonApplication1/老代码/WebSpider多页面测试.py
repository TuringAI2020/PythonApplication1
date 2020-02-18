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
import _thread
import threading
r=RClient.GetInst()

chrome_opt = Options()      # 创建参数设置对象.
#chrome_opt.add_argument('--headless')   # 无界面化.
#chrome_opt.add_argument('--disable-gpu')    # 配合上面的无界面化.
#chrome_opt.add_argument('--window-size=400,1080')   # 设置窗口大小, 窗口大小会有影响.
chrome = webdriver.Chrome( chrome_options=chrome_opt)
chrome.implicitly_wait(10) 
locker = threading.Lock()

def Open(urlArr,targs,callback):        
    index = len(chrome.window_handles)-1
    chrome.switch_to.window(chrome.window_handles[0])
    for turl in urlArr:
        print("准备打开 %s"%turl) 
        js = "window.open('%s');"%turl
        chrome.execute_script(js) 
        print("正在打开 %s"%turl)  

    count = len(chrome.window_handles)
    canClose=(count==(len(urlArr)+1))
    while canClose==True: 
        chrome.switch_to.window(chrome.window_handles[0])
        callback({"Url":chrome.current_url,"PageSource":len(chrome.page_source)})
        chrome.close()   
        count = len(chrome.window_handles) 
        canClose=(1 != count)
        print("剩余 %s"%count)
 

print("OK")
def Callback(task):
    print(task)
urlArr=[]
for k in range(10):
    urlArr.append("https://www.baidu.com/s?wd=%s"%k) 
Open(urlArr,None,Callback)
 