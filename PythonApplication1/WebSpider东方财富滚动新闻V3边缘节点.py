import requests
import json
import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from CONVERTOR import CONVERT
from CHECKER import  CHECKER 
import  urllib   
import codecs
from HtmlConvertor import HtmlConvertor
import random
import datetime

chrome_opt = Options()      # 创建参数设置对象.
chrome_opt.add_argument('--headless')   # 无界面化.
chrome_opt.add_argument('--disable-gpu')    # 配合上面的无界面化.
chrome_opt.add_argument('--window-size=400,1080')   # 设置窗口大小, 窗口大小会有影响.
chrome = webdriver.Chrome( chrome_options=chrome_opt)
chrome.implicitly_wait(10)
 
 
def ProcWebData():
    #serverUrl="http://122.51.159.248/YunStock2Service?keyName=BXCGMXURL&taskId=%s"%taskId
    serverUrl = "http://127.0.0.1:80/YunStock2Service"
    while True:
        try: 
            #url="https://kuaixun.eastmoney.com/"
            url="https://kuaixun.eastmoney.com/qqyh.html"

            name="东方财富网快讯"
            chrome.get(url)  
            time.sleep(5)
            chrome.switch_to_window(chrome.window_handles[0]) 
            list = chrome.find_element_by_id("livenews-list").find_elements_by_class_name("livenews-media")
            postArr=[]
            for listItem in list:
                listItem_id=listItem.get_attribute("id").split("-")[-1]
                year=listItem_id[:4]
                month=listItem_id[4:6]
                day=listItem_id[6:8]
                arr=listItem.text.split()
                date =  "%s-%s-%s"%(year,month,day)
                dateTime = "%s %s:00"%(date,arr[0])
                content="%s %s"%(date,listItem.text.strip())
                href="" 
                innerHtml=listItem.get_attribute("innerHTML")
                if True == CHECKER.Contains(innerHtml,"href="):
                    href=listItem.find_element_by_tag_name("a").get_attribute("href")
                item={"Source":name,"PublishTime":dateTime,"Content":content,"Href":href}
                print(item)
                postArr.append(item)
            post_data={"keyName":"SHORTNEWS","jsonReq": json.dumps({"Name":name,"Url":url},ensure_ascii=False),"jsonRes": json.dumps(postArr,ensure_ascii=False)}
            res2 = requests.post(serverUrl,data=post_data)
            print("POST %s \r\n RES %s \r\n --------- \r\n"%(post_data,res2.text))
            time.sleep(3000)
        except BaseException as e:
            print(" 异常 %s " % e)
            time.sleep(6000)
    pass
ProcWebData()
spider.Quit()
print("全部结束")
 