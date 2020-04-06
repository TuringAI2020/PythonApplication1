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
  
from CHECKER import CHECKER
from HtmlConvertor import HtmlConvertor
import requests

#res = requests.get("http://www.gov.cn/premier/2020-03/17/content_5492396.htm")
#html = res.text.encode(res.encoding).decode('utf-8')
#inst = HtmlConvertor.GetInst().LoadFromString(html)
#jsonData = inst.ConvertToJson()
#tag = inst.FindSectionOne(".pages-date")
#title = inst.FindSectionOne(".article h1")
#arr = re.split("来源：|【字体：", tag["Text"])
#date = "%s:00"%arr[0].strip()
#source = arr[1].strip()
import CONVERTOR

res = requests.get("http://www.gov.cn/xinwen/yaowen.htm")
html = res.text.encode(res.encoding).decode('utf-8')
inst = HtmlConvertor.GetInst().LoadFromString(html)
jsonData = inst.ConvertToJson()
jsonData = json.loads(jsonData)
links = jsonData["Links"]
links = list(filter(lambda x: True == CHECKER.Contains(x["Href"],"content_"),links))
serverUrl="http://127.0.0.1:5000/YunStock2Service"
for link in links:
    postArr=[]
    href="http://www.gov.cn/%s"%link["Href"]
    res = requests.get(href)
    html = res.text.encode(res.encoding).decode('utf-8')
    article=inst.LoadFromString(html).ConvertToJson()
    article = json.loads(article)
    if 30<len(article["Article"]):
        tag = inst.FindSectionOne(".pages-date")
        title = inst.FindSectionOne(".article h1")
        arr = re.split("来源：|【字体：", tag["Text"])
        date = "%s:00"%arr[0].strip()
        source = arr[1].strip()
        title=title["Text"].strip()
        article = article["Article"].strip()
        item ={
            "Title":title,
            "Content":article,
            "PublishTime":date,
            "DateTag":CONVERTOR.CONVERT.DateToInt(date),
            "Status":1,
            "DataSource":source,
            "Href":href
        }
        postArr.append(item)
        post_data={"keyName":"ARTICLE","jsonReq": json.dumps({"Title":title,"Url":href},ensure_ascii=False),"jsonRes": json.dumps(postArr,ensure_ascii=False)}
        print(post_data)
        res2 = requests.post(serverUrl,data=post_data)
        print("POST %s \r\n RES %s \r\n --------- \r\n"%(post_data,res2.text))
        time.sleep(10)

