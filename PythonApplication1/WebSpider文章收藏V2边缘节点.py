import requests
import json
import time
#from selenium import webdriver
#from selenium.webdriver.support.select import Select
#from selenium.webdriver.chrome.options import Options
from ChromeSpider2 import ChromeSpider2
from CONVERTOR import CONVERT
from CHECKER import  CHECKER
import  urllib   
import codecs
import datetime

spider = ChromeSpider2() 
def ProcWebData():
    taskId = "Task0"
    #serverUrl="http://122.51.159.248:5000/YunStock2Service?keyName=ARTICLE&taskId=%s" % taskId
    serverUrl = "http://127.0.0.1:5000/YunStock2Service?keyName=ARTICLE&taskId=%s" % taskId
    count=0
    while True:
        try:
            res = requests.get(serverUrl)
            print("接收 %s \r\n --------\r\n" % res.text)
            res = json.loads(res.text)
            if(res["success"] == True):
                data = res["data"]
                if 10 <= len(data):
                    data = json.loads(data) 
                    url = data["Url"]  

                    resArr = []
                    jsonStr = spider.LoadWeb(url,"文章收藏").GetDataFromWeb() 

                    if jsonStr != None:
                        jsonData = json.loads(jsonStr)
                        title=jsonData["Title"]
                        content=jsonData["Content"]
                        publishTime =datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        dateTag = CONVERT.DateToInt(publishTime)
                        item={
                                "Title":title,
                                "Content":content,
                                "PublishTime":publishTime
                            }
                    #post_data = {"taskId":taskId,"keyName":"JGDYLB","jsonReq": json.dumps(data,ensure_ascii=False),"jsonRes": json.dumps(resArr,ensure_ascii=False)}
                    #res2 = requests.post(serverUrl,data=post_data)
                    #print("POST %s \r\n RES %s \r\n --------- \r\n" % (post_data,res2.text))
 
            else:
                time.sleep(3)
        except BaseException as e:
            print(" 异常 %s " % e)
            time.sleep(20)
    pass
ProcWebData()
spider.Quit()
print("全部结束")
 