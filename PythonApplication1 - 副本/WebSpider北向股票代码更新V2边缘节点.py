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
 
chrome_opt = Options()      # 创建参数设置对象.
chrome_opt.add_argument('--headless')   # 无界面化.
chrome_opt.add_argument('--disable-gpu')    # 配合上面的无界面化.
chrome_opt.add_argument('--window-size=400,400')   # 设置窗口大小, 窗口大小会有影响.
chrome = webdriver.Chrome( chrome_options=chrome_opt) 
timeTag = time.strftime("%Y-%m-%d", time.localtime())
 
def Download北向Code(): 
    url = "http://data.eastmoney.com/hsgtcg/list.html"# 沪深港通持股

    chrome.get(url) 
    time.sleep(5)
    closebtn=chrome.find_element_by_id("intellcontclose")
    closebtn.click()

    linkBtn = chrome.find_element_by_link_text("下一页")
    clsVal = linkBtn.get_attribute('class')
    pageIndex = 0
    while clsVal != "nolink": 
        chrome.switch_to_window(chrome.window_handles[0]) 
        linkBtn = chrome.find_element_by_link_text("下一页")
        chrome.execute_script("arguments[0].scrollIntoView(false);",linkBtn)
        clsVal = linkBtn.get_attribute('class')
        jsonStr = HtmlConvertor.GetInst().LoadFromString(html=chrome.page_source).ConvertToJson() 
        jsonData=json.loads(jsonStr)
        if ("Tables" in jsonData and []!=jsonData["Tables"]):
            rows = jsonData["Tables"][0]["body"]
            postArr=[]
            for row in rows:
                code=row[1]
                name=row[2]
                if (6 == len(code) and 0<len(name)): 
                    print("%s %s"%(code,name))
                    item={"Code":code,"Name":name,"Sort":3}
                    postArr.append(item)
            print("页码 %d"%pageIndex)
            serverUrl="http://122.51.159.248/YunStock2Service?keyName=BXCODE"
            #serverUrl="http://127.0.0.1:80/YunStock2Service?keyName=BXCODE"
            post_data={"keyName":"BXCODE",  "jsonReq": json.dumps({},ensure_ascii=False),"jsonRes": json.dumps(postArr,ensure_ascii=False)}
            res2 = requests.post(serverUrl,data=post_data)
            print("POST %s \r\n RES %s \r\n --------- \r\n"%(post_data,res2.text))

        else:
            print("%d 页数据未能加载"%pageIndex)
            time.sleep(20)
            pass
        pageIndex+=1
        linkBtn.click()
        time.sleep(random.uniform(3,6))
    chrome.quit()


     
Download北向Code() 
print("OK")