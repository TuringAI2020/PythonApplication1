import os
import random
import time
import sys 
import io  #StringIO模块就是在内存中读写str
import re
import json
import requests

 
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options 
from CHECKER import CHECKER
from HtmlConvertor import HtmlConvertor 
from urllib import parse
 
chrome_opt = Options()      # 创建参数设置对象.
chrome_opt.add_argument('--headless')   # 无界面化.
chrome_opt.add_argument('--disable-gpu')    # 配合上面的无界面化.
chrome_opt.add_argument('--window-size=400,400')   # 设置窗口大小, 窗口大小会有影响.
chrome = webdriver.Chrome( chrome_options=chrome_opt) 
timeTag = time.strftime("%Y-%m-%d", time.localtime())
 
def Download所有机构(): 
    url = "http://data.eastmoney.com/hsgtcg/InstitutionQueryMore.aspx"# 沪深港通持股

    chrome.get(url)  
    jsonStr = HtmlConvertor.GetInst().LoadFromString(html=chrome.page_source).ConvertToJson() 
    jsonData = json.loads(jsonStr)
    links = jsonData["Links"]
    links = list(filter(lambda x:CHECKER.StartWith(x["Href"],"/hsgtcg/InstitutionhdStatistics.aspx\?jgCode="),links))
    postArr=[]
    for link in links:
        href="http://data.eastmoney.com%s"%link["Href"]
        name=link["Title"] if len(link["Title"]) > len(link["Text"]) else link["Text"]
        params = parse.parse_qs(parse.urlparse(href).query)
        jpCode = params["jgCode"][0]
        jpName = params["jgName"][0]
        item={"jgCode":jpCode,"jgName":jpName,"Href":href,"Sort":0}
        print(item)
        postArr.append(item)
    serverUrl="http://122.51.159.248/YunStock2Service?keyName=JG"
    #serverUrl="http://127.0.0.1:80/YunStock2Service?keyName=JG"
    post_data={"keyName":"JG",  "jsonReq": json.dumps({},ensure_ascii=False),"jsonRes": json.dumps(postArr,ensure_ascii=False)}
    res2 = requests.post(serverUrl,data=post_data)
    print("POST %s \r\n RES %s \r\n --------- \r\n"%(post_data,res2.text))

    chrome.quit()


     
Download所有机构() 
print("OK")