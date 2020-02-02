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

# 1.  导入Python SSL处理模块
import ssl
import jieba

from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from ChromeSpider import ChromeSpider
from CHECKER import CHECKER
from RClient import RClient

def callback(input,args):
     output = input
     title = input["Title"]
     if True == CHECKER.HasHanZi(title):
         dateTag = time.strftime("%Y%m%d", time.localtime())
         output["Name"] =  args["Name"]
         output["Code"] =  args["Code"]
         output["DateTag"] = dateTag
         output["PageTag"] = args["PageTag"]
         return output
     else:
         qName="FailDownload"
         RClient.GetInst().QueueEn(qName,args)
         return None

         pass

chrome_opt = Options()      # 创建参数设置对象.
chrome_opt.add_argument('--headless')   # 无界面化.
chrome_opt.add_argument('--disable-gpu')    # 配合上面的无界面化.
chrome_opt.add_argument('--window-size=400,1080')   # 设置窗口大小, 窗口大小会有影响.
chrome = webdriver.Chrome( chrome_options=chrome_opt)
spider = ChromeSpider()
timeTag = time.strftime("%Y-%m-%d", time.localtime())
 
def DownloadAllCode(): 
    url = "http://data.eastmoney.com/zjlx/detail.html"

    chrome.get(url)  
    linkBtn = chrome.find_element_by_link_text("下一页")
    clsVal = linkBtn.get_attribute('class')
    pageIndex = 0
    while clsVal != "nolink": 

        trArr = chrome.find_element_by_id("dt_1").find_elements_by_tag_name("tr")
     
        trArrLength = len(trArr)
        index = 0
        while index < trArrLength:
            tr = trArr[index]
            aArr = tr.find_elements_by_tag_name("a")
            if(5==len(aArr) and len(aArr[0].text)==6 and len(aArr[1].text)<=4):
                href1 = aArr[0].get_attribute('href') 
                href2 = aArr[1].get_attribute('href') 
                isValidHref1 = re.match(r'^http://quote.eastmoney.com/\d{6}.html$', href1)
                isValidHref2 = re.match(r'^http://data.eastmoney.com/stockdata/\d{6}.html$', href2)
                if isValidHref1 and isValidHref2:     
                    code = aArr[0].text.strip()
                    code2 = code
                    name = aArr[1].text.replace("*","@").strip() 
                    print("%s %s %s"%(pageIndex,code,name))
                    if code[0] == 6:
                        code2="SH"+code
                    else:
                        code2="SZ"+code
                    #http://data.eastmoney.com/stockdata/300073.html #综合信息
                    #http://f10.eastmoney.com/f10_v2/BusinessAnalysis.aspx?code=SZ300073 #经营分析 主营范围 没能抓出来 OK
                    #http://f10.eastmoney.com/f10_v2/FinanceAnalysis.aspx?code=SZ300073 #新财务分析 百分比报表没取出来 OK
                    #http://data.eastmoney.com/executive/300073.html #高管持股 OK
                    #http://data.eastmoney.com/executive/gdzjc/300073.html #股东增减持 日期不足取title OK
                    #http://data.eastmoney.com/dxf/q/300073.html #限售解禁
                    #http://data.eastmoney.com/gdhs/detail/300073.html #股东户数 OK
                    #http://f10.eastmoney.com/f10_v2/ShareholderResearch.aspx?code=SZ300073 #股东研究
                    #http://data.eastmoney.com/zlsj/detail/300073.html #主力持仓 OK
                    #http://data.eastmoney.com/jgdy/gsjsdy/300073.html #机构调研 OK
                    #http://data.eastmoney.com/bgcz/detail/300073.html #并购重组 OK
                    #http://data.eastmoney.com/notices/stock/300073.html #公告大全 OK
                    #http://data.eastmoney.com/dzjy/detail/300073.html #大宗交易 OK
                    #http://data.eastmoney.com/stockcomment/300073.html #千股千评
                    #http://data.eastmoney.com/stock/lhb/lcsb/300073.html #龙虎榜单 历次上榜
                    #http://data.eastmoney.com/rzrq/detail/300073.html #融资融券 OK
                    #http://f10.eastmoney.com/f10_v2/CoreConception.aspx?code=SZ300073 #核心题材 OK
                    #http://data.eastmoney.com/zjlx/002050.html #资金流向 OK

                    hrefArr=[
                        {"PageTag":"综合信息","Url":"http://data.eastmoney.com/stockdata/%s.html"%code,"Name":name,"Code":code,"Code2":code2}
                       ,{"PageTag":"经营分析","Url":"http://f10.eastmoney.com/f10_v2/BusinessAnalysis.aspx?code=%s"%code2,"Name":name,"Code":code,"Code2":code2}
                       ,{"PageTag":"新财务分析","Url":"http://f10.eastmoney.com/f10_v2/FinanceAnalysis.aspx?code=%s"%code2,"Name":name,"Code":code,"Code2":code2}
                       ,{"PageTag":"高管持股","Url":"http://data.eastmoney.com/executive/%s.html"%code,"Name":name,"Code":code,"Code2":code2} 
                       ,{"PageTag":"股东增减持","Url":"http://data.eastmoney.com/executive/gdzjc/%s.html"%code,"Name":name,"Code":code,"Code2":code2} 
                       ,{"PageTag":"限售解禁","Url":"http://data.eastmoney.com/dxf/q/%s.html"%code,"Name":name,"Code":code,"Code2":code2} 
                       ,{"PageTag":"股东户数","Url":"http://data.eastmoney.com/gdhs/detail/%s.html"%code,"Name":name,"Code":code,"Code2":code2} 
                       ,{"PageTag":"股东研究","Url":"http://f10.eastmoney.com/f10_v2/ShareholderResearch.aspx?code=%s"%code2,"Name":name,"Code":code,"Code2":code2} 
                       ,{"PageTag":"主力持仓","Url":"http://data.eastmoney.com/zlsj/detail/%s.html"%code,"Name":name,"Code":code,"Code2":code2}  
                       ,{"PageTag":"机构调研","Url":"http://data.eastmoney.com/jgdy/gsjsdy/%s.html"%code,"Name":name,"Code":code,"Code2":code2}  
                       ,{"PageTag":"并购重组","Url":"http://data.eastmoney.com/bgcz/detail/%s.html"%code,"Name":name,"Code":code,"Code2":code2}
                       ,{"PageTag":"公告大全","Url":"http://data.eastmoney.com/notices/stock/%s.html"%code,"Name":name,"Code":code,"Code2":code2}  
                       ,{"PageTag":"大宗交易","Url":"http://data.eastmoney.com/dzjy/detail/%s.html"%code,"Name":name,"Code":code,"Code2":code2}  
                       ,{"PageTag":"千股千评","Url":"http://data.eastmoney.com/stockcomment/%s.html"%code,"Name":name,"Code":code,"Code2":code2}  
                       ,{"PageTag":"龙虎榜单历次上榜","Url":"http://data.eastmoney.com/stock/lhb/lcsb/%s.html"%code,"Name":name,"Code":code,"Code2":code2}  
                       ,{"PageTag":"融资融券","Url":"http://data.eastmoney.com/rzrq/detail/%s.html"%code,"Name":name,"Code":code,"Code2":code2}  
                       ,{"PageTag":"核心题材","Url":"http://f10.eastmoney.com/f10_v2/CoreConception.aspx?code=%s"%code2,"Name":name,"Code":code,"Code2":code2}  
                       ,{"PageTag":"资金流向","Url":"http://data.eastmoney.com/zjlx/%s.html"%code,"Name":name,"Code":code,"Code2":code2}  
                        ]
                    for href in hrefArr:
                        qName="股票:待下载页面队列"
                        RClient.GetInst().QueueEn(qName,href)
                        print(href)
                    #spider.LoadWeb(href).SaveDataToRedis(callback) 

            index+=1 
        chrome.switch_to_window(chrome.window_handles[0]) 
        linkBtn = chrome.find_element_by_link_text("下一页")
        chrome.execute_script("arguments[0].scrollIntoView(false);",linkBtn)
        clsVal = linkBtn.get_attribute('class')
        linkBtn.click()
        pageIndex+=1
        print("页码 %s"%pageIndex)

       # time.sleep(random.uniform(10,20))
    chrome.quit()

def CallbackDownloadDetail(qName,item):
    data=json.loads(item)
    href=data["Url"]
    spider.LoadWeb(href,data).SaveDataToRedis(callback) 
    qName="股票:待下载页面队列"
    itemCount = RClient.GetInst().Count(qName)
    print("已下载 %d %s "%(itemCount,item))

    pass
def DownloadDetailPage():
    qName="股票:待下载页面队列"
    RClient.GetInst().ProcQueue(qName,CallbackDownloadDetail)
    pass
#DownloadAllCode()
DownloadDetailPage()
print("OK")