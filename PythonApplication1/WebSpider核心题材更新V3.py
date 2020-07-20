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
 
def 核心题材数据更新回调函数(dictName,code): 
    code2="SH"+code if code[0]=="6" else "SZ"+code
    url = "http://f10.eastmoney.com/f10_v2/CoreConception.aspx?code=%s"%code2 #核心题材
    jsonStr = spider.LoadWeb(url,"核心题材").GetDataFromWeb()
    jsonData=json.loads(jsonStr)
    if 0<len(jsonData["Article"]):
        article=jsonData["Article"]
        sections = list(filter(lambda k:len(k.strip())>0,article.split("\n")))
        for section in sections:
            section=section.strip()
            words = re.split("\s|:",section)
            words = list(filter(lambda k:len(k.strip())>0,words))
            是否是所属板块 = CHECKER.Contains(section,"所属板块")
            for word in  words:
                if (True== 是否是所属板块 and( False == CHECKER.Contains(word,"要点") and False == CHECKER.Contains(word,"所属板块"))):
                    word=word.strip()
                    r.SortDictSave("Stock:Relation:Conception:%s"%word,code,0)
                    print("保存核心题材 %s %s"%(code,word))
                    pass
            if  True == CHECKER.Contains(words[0],"要点"):
                r.DictSave("Stock:Detail:%s"%code,"核心题材:"+words[1].strip(),section)
                print("保存核心题材 %s %s"%(code,words[1]))
                pass
    #    time.sleep(random.uniform(2,4))
    #chrome.quit()
      
r.TraverseDict("Stock:BaseData:AllCode",核心题材数据更新回调函数)
print("OK")
chrome.quit()
spider.Quit()