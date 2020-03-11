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
 
 
def ProcWebData(name,url):
    #serverUrl="http://122.51.159.248/YunStock2Service"
    serverUrl = "http://127.0.0.1:80/YunStock2Service" 
    try: 
        #url="https://kuaixun.eastmoney.com/"
        #url="https://kuaixun.eastmoney.com/qqyh.html"

        #name="东方财富网快讯"
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
            _time=listItem.find_element_by_class_name("time").text.strip()
            arr=listItem.text.split()
            date =  "%s-%s-%s"%(year,month,day)
            dateTime = "%s %s:00"%(date,_time)
            content="%s %s"%(date,listItem.text.strip())
            href="" 
            innerHtml=listItem.get_attribute("innerHTML")
            if True == CHECKER.Contains(innerHtml,"href="):
                href=listItem.find_element_by_tag_name("a").get_attribute("href")
            item={"Source":name,"PublishTime":dateTime,"Content":content,"Href":href}
            #print("%s%s"%(name,dateTime))
            postArr.append(item)
        post_data={"keyName":"SHORTNEWS","jsonReq": json.dumps({"Name":name,"Url":url},ensure_ascii=False),"jsonRes": json.dumps(postArr,ensure_ascii=False)}
        print(post_data)
        res2 = requests.post(serverUrl,data=post_data)
        print("POST %s \r\n RES %s \r\n --------- \r\n"%(post_data,res2.text))
    except BaseException as e:
        print(" 异常 %s " % e)
        time.sleep(60)
    pass

while True:
    ProcWebData("债券","https://kuaixun.eastmoney.com/zq.html")
    ProcWebData("外汇","https://kuaixun.eastmoney.com/wh.html")
    ProcWebData("商品","https://kuaixun.eastmoney.com/sp.html")
    ProcWebData("全球股市","https://kuaixun.eastmoney.com/qqgs.html")
    ProcWebData("经济数据","https://kuaixun.eastmoney.com/jjsj.html")
    ProcWebData("全球央行","https://kuaixun.eastmoney.com/qqyh.html")
    ProcWebData("地区","https://kuaixun.eastmoney.com/dq.html")
    ProcWebData("上市公司","https://kuaixun.eastmoney.com/ssgs.html")
    ProcWebData("焦点","https://kuaixun.eastmoney.com/yw.html")
    ProcWebData("滚动","https://kuaixun.eastmoney.com/")
    time.sleep(1800)
spider.Quit()
print("全部结束")
 