import requests
import json
import time
import datetime
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from CONVERTOR import CONVERT
from CHECKER import  CHECKER 
import  urllib   
import codecs
from HtmlConvertor import HtmlConvertor
import random

chrome_opt = Options()      # 创建参数设置对象.
chrome_opt.add_argument('--headless')   # 无界面化.
chrome_opt.add_argument('--disable-gpu')    # 配合上面的无界面化.
chrome_opt.add_argument('--window-size=1920,1080')   # 设置窗口大小, 窗口大小会有影响.
chrome = webdriver.Chrome( chrome_options=chrome_opt)
chrome.implicitly_wait(10)

def AddToArray(jgCode,jgName,targetArr):
    jsonStr = HtmlConvertor.GetInst().LoadFromString(chrome.page_source).ConvertToJson()
    jsonData=json.loads(jsonStr)
    tables = jsonData["Tables"]
    rows = tables[len(tables)-1]["body"]
    for row in rows:
        if 12 == len(row): 
            持股日期Tag=CONVERT.DateToInt(row[0])
            item={ 
                    "持股日期":row[0]
                    ,"持股日期Tag":持股日期Tag
                    ,"Code":row[1]
                    ,"股票简称":row[2]
                    ,"当日收盘价":CONVERT.StrToFloat(row[3])
                    ,"当日涨跌幅":CONVERT.StrToFloat(row[4])
                    ,"机构名称":jgName
                    ,"jgCode":jgCode
                    ,"持股数量":CONVERT.UnitStrToFloat(row[6])
                    ,"持股市值":CONVERT.UnitStrToFloat(row[7])
                    ,"持股数量占A股百分比":CONVERT.StrToFloat(row[8])
                    ,"持股市值变化1日":CONVERT.UnitStrToFloat(row[9])
                    ,"持股市值变化5日":CONVERT.UnitStrToFloat(row[10])
                    ,"持股市值变化10日":CONVERT.UnitStrToFloat(row[11])
                    }
            targetArr.append(item)
    return targetArr

 
def ProcWebData():
    while True:
        currentDay = datetime.datetime.now()
        #taskId = CONVERT.StrToInt(currentDay.strftime("%Y%m%d"))-1
        taskId = 20200504
        serverUrl="http://122.51.159.248:5000/YunStock2Service?keyName=BXCGMXURL&taskId=%s"%taskId
        #serverUrl = "http://127.0.0.1:5000/YunStock2Service?keyName=BXCGMXURL&taskId=%s"%taskId
        try:
            res = requests.get(serverUrl)
            print("接收 %s \r\n --------\r\n" % res.text)
            res = json.loads(res.text)
            if(res["success"] == True):
                data = res["data"]
                if 10 <= len(data):
                    data = json.loads(data) 
                    DateTag = data["DateTag"]
                    Date = data["Date"]
                    jgCode = data["jgCode"]
                    jgName = data["jgName"]
                    url = data["Url"] 
                    chrome.get(url)  
                    time.sleep(random.uniform(2,5))
                    postArr=[]
                    pageIndex = 0
                    if True != CHECKER.Contains(chrome.page_source,"下一页"):
                        postArr=AddToArray(jgCode,jgName,postArr)
                        print("单页数据 %s"%postArr)
                        pass

                    if True == CHECKER.Contains(chrome.page_source,"下一页"):
                        chrome.switch_to_window(chrome.window_handles[0]) 
                        linkBtn = chrome.find_element_by_link_text("下一页") 
                        clsVal = linkBtn.get_attribute('class')
                        #closebtn=chrome.find_element_by_id("intellcontclose")
                        #closebtn.click()
                        while False == CHECKER.Contains(clsVal,"nolink"):  
                            chrome.switch_to_window(chrome.window_handles[0]) 
                            linkBtn = chrome.find_element_by_link_text("下一页")
                            chrome.execute_script("arguments[0].scrollIntoView(false);",linkBtn)
                            postArr=AddToArray(jgCode,jgName,postArr)
                            print("多页数据 %s %s %s"%(jgCode,jgName,pageIndex))
                            pageIndex+=1
                            linkBtn = chrome.find_element_by_link_text("下一页")
                            linkBtn.click()
                            time.sleep(random.uniform(3,5))
                            style = chrome.find_element_by_class_name("content").find_element_by_tag_name("div").get_attribute("style")
                            subCount=5
                            while True != CHECKER.Contains(style,"none") and 0<subCount:
                                print("还在加载中...%s %s"%(pageIndex,subCount))
                                subCount-=1
                                time.sleep(random.uniform(3,5))
                                style = chrome.find_element_by_class_name("content").find_element_by_tag_name("div").get_attribute("style")
                                
                            linkBtn = chrome.find_element_by_link_text("下一页")
                            clsVal = linkBtn.get_attribute('class')
                        pass

                    post_data={"taskId":taskId,"keyName":"BXCGMXURL","jsonReq": json.dumps(data,ensure_ascii=False),"jsonRes": json.dumps(postArr,ensure_ascii=False)}
                    res2 = requests.post(serverUrl,data=post_data)
                    print("POST %s \r\n RES %s \r\n --------- \r\n"%(post_data,res2.text))

            else:
                time.sleep(3)
        except BaseException as e:
            print(" 异常 %s " % e)
            time.sleep(20)
    pass
ProcWebData() 
print("全部结束")
 