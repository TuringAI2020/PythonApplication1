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
#article = json.loads(jsonData)["Article"]
#print(article)

res = requests.get("http://www.gov.cn/xinwen/yaowen.htm")
html = res.text.encode(res.encoding).decode('utf-8')
inst = HtmlConvertor.GetInst().LoadFromString(html)
jsonData = inst.ConvertToJson()
jsonData = json.loads(jsonData)
links = jsonData["Links"]
links = list(filter(lambda x: True == CHECKER.Contains(x["Href"],"content_"),links))
for link in links:
    href="http://www.gov.cn/%s"%link["Href"]
    res = requests.get(href)
    html = res.text.encode(res.encoding).decode('utf-8')
    article=inst.LoadFromString(html).ConvertToJson()
    article = json.loads(article)
    tag = inst.FindSectionOne(".pages-date")
    title = inst.FindSectionOne(".article h1")
    arr = re.split("来源：|【字体：", tag["Text"])
    date = "%s:00"%arr[0].strip()
    source = arr[1].strip()
    print("%s\r\n%s\r\n%s\r\n"%(title["Text"].strip(),source.strip(),date.strip()))
    print(article["Article"])

