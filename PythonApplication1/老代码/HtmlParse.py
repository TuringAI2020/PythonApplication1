import sys
import os
import re
from bs4 import BeautifulSoup
import redis
import json
#from selenium import webdriver
#from selenium.webdriver.support.select import Select
#webDriver = webdriver.Chrome()
redisclient = redis.Redis(host='localhost', port=6379, db=0)
for root, dirs,files in os.walk("E:\\原始数据源\\中国政府网_滚动_正文\\"):
    for file in files:
        filePath = root + "\\" + file 
        fs = open(filePath,"r",encoding="utf-8")
        html = fs.read()
        fs.close()
        soup = BeautifulSoup(html)
        title = soup.h1.string
        date = soup.find('div',{'class':'pages-date'}).text
        content = soup.find(id="UCAP-CONTENT").text
        item = {'Title':title,'Date':date,'Content':content,'Path':file}
        redisclient.rpush("中国政府网_滚动_正文",json.dumps(item))
        print(file) 
redisclient.close();
print('全部结束')
