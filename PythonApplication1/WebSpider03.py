import sys
import os
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.select import Select
webDriver = webdriver.Chrome()

for root, dirs,files in os.walk("E:\\原始数据源\\中国政府网_滚动\\"):
    for file in files:
        filePath = root + "\\" + file
        #print(root+"\\"+file)
        fs = open(filePath,"r",encoding="utf-8")
        html = fs.read()
        fs.close()
        soup = BeautifulSoup(html)
        alist = soup.find_all("a")
        i = 0
        while i < len(alist):
            href = alist[i].attrs["href"]
            #print(href)
            if re.match("^http://www.gov.cn/xinwen/", href, flags=0):
                try:
                    print(str(len(alist))+"-"+str(i)+" "+href)
                    webDriver.get(href)
                    html = webDriver.page_source
                    #fs =  open("E:\\原始数据源\\中国政府网_滚动_正文\\"+str(i)+".txt",encoding="utf-8",mode="w")
                    fs =  open("E:\\原始数据源\\中国政府网_滚动_正文\\"+href.replace('/','~').replace(':','+')+".txt",encoding="utf-8",mode="w")
                    fs.write(html)
                    fs.close()
                except Exception as e:
                    print(e)
                finally:
                    print(href)

            i += 1 
             
