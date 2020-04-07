import requests
import json
import time
#from selenium import webdriver
#from selenium.webdriver.support.select import Select
#from selenium.webdriver.chrome.options import Options
from ChromeSpider import ChromeSpider
from CONVERTOR import CONVERT
from CHECKER import  CHECKER
import  urllib   
import codecs

spider = ChromeSpider() 
def ProcWebData():
    taskId = "Task0"
    serverUrl="http://122.51.159.248:5000/YunStock2Service?keyName=JGDYLB&taskId=%s" % taskId
    #serverUrl = "http://127.0.0.1:5000/YunStock2Service?keyName=JGDYLB&taskId=%s" % taskId
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
                    code = data["Code"]

                    resArr = []
                    jsonStr = spider.LoadWeb(url,"机构调研列表").GetDataFromWeb() 
                    jsonData = json.loads(jsonStr)
                    if "Tables" in jsonData: 
                        tables = jsonData["Tables"]
                        if 0 < len(tables):
                            rows = tables[len(tables) - 1]["body"]
                            for row in rows:
                                if 10 == len(row): 
                                    持股日期Tag = CONVERT.DateToInt(row[0]) 
                                    item = { 
                                             "Code":code
                                            ,"接待机构数量":CONVERT.StrToInt(row[4])
                                            ,"接待方式":row[5]
                                            ,"接待人员":row[6] 
                                            ,"接待地点":row[7]
                                            ,"接待日期":row[8]
                                            ,"公告日期":row[9]
                                            ,"接待日期Tag":CONVERT.DateToInt(row[8])
                                            ,"公告日期Tag":CONVERT.DateToInt(row[9])
                                            }
                                    resArr.append(item)
                    post_data = {"taskId":taskId,"keyName":"JGDYLB","jsonReq": json.dumps(data,ensure_ascii=False),"jsonRes": json.dumps(resArr,ensure_ascii=False)}
                    res2 = requests.post(serverUrl,data=post_data)
                    print("POST %s \r\n RES %s \r\n --------- \r\n" % (post_data,res2.text))
 
            else:
                time.sleep(3)
        except BaseException as e:
            print(" 异常 %s " % e)
            time.sleep(20)
    pass
ProcWebData()
spider.Quit()
print("全部结束")
 