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
    #serverUrl="http://122.51.159.248:5000/YunStock2Service?keyName=GJDCGGK&taskId=%s" % taskId
    serverUrl = "http://127.0.0.1:5000/YunStock2Service?keyName=GJDCGGK&taskId=%s" % taskId
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
                    params = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)  

                    resArr = []
                    jsonStr = spider.LoadWeb(url,"国家队持股概况").GetDataFromWeb() 
                    jsonData = json.loads(jsonStr)
                    if "Tables" in jsonData: 
                        tables = jsonData["Tables"]
                        if 0 < len(tables):
                            rows = tables[len(tables) - 1]["body"]
                            for row in rows:
                                if 8 == len(row): 
                                    报告期Tag = CONVERT.DateToInt(row[0])
                                    item = {  
                                             "报告期":row[0]
                                            ,"报告期Tag":报告期Tag
                                            ,"持股数量":CONVERT.StrToInt(row[2])
                                            ,"持股市值":CONVERT.UnitStrToFloat(row[3])
                                            ,"持股占市场总和比例":CONVERT.UnitStrToFloat(row[4])
                                            ,"持有个股数量":CONVERT.StrToInt(row[5])
                                            ,"沪深300指数":CONVERT.UnitStrToFloat(row[6])
                                            ,"涨跌幅":CONVERT.UnitStrToFloat(row[7])
                                            }
                                    resArr.append(item)
                    post_data = {"taskId":taskId,"keyName":"GJDCGGK","jsonReq": json.dumps(data,ensure_ascii=False),"jsonRes": json.dumps(resArr,ensure_ascii=False)}
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
 