print("加载网页抓取模块")
from selenium import webdriver
from selenium.webdriver.support.select import Select
import time

url = "http://sousuo.gov.cn/column/30611/{page}.htm"
webDriver = webdriver.Chrome()

 
count=5255
index = 0
while index < count:
    cur_url=url.replace("{page}",str(index))
    webDriver.get(cur_url)
    #webDriver.execute_script('setTimeout(()=>{document.querySelectorAll(".bd_topic a")['+str(count)+'].click()},3000)')
    #print(webDriver.page_source)
    html = webDriver.page_source
    index = index + 1
    fs = open("E:\\原始数据源\\中国政府网_滚动\\"+str(index)+".txt",encoding="utf-8",mode="w")
    fs.write(html)
    fs.close()
    print(index-1)
    #time.sleep(3)