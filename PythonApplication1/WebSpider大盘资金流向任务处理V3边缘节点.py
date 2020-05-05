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
    serverUrl="http://122.51.159.248:5000/YunStock2Service?keyName=DPZJLX&taskId=%s" % taskId
    #serverUrl = "http://127.0.0.1:5000/YunStock2Service?keyName=DPZJLX&taskId=%s" % taskId
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
                    jsonStr = spider.LoadWeb(url,"大盘资金流向").GetDataFromWeb() 
                    jsonData = json.loads(jsonStr)
                    if "Tables" in jsonData: 
                        tables = jsonData["Tables"]
                        if 0 < len(tables):
                            rows = tables[len(tables) - 1]["body"]
                            for row in rows:
                                if 15 == len(row): 
                                    日期Tag = CONVERT.DateToInt(row[0])
                                    item = {  
                                             "日期":row[0]
                                            ,"日期Tag":日期Tag
                                            ,"上证收盘价":CONVERT.StrToFloat(row[1]) 
                                            ,"上证涨跌幅":CONVERT.UnitStrToFloat(row[2]) 
                                            ,"深证收盘价":CONVERT.StrToFloat(row[3]) 
                                            ,"深证涨跌幅":CONVERT.UnitStrToFloat(row[4])
                                            ,"主力净流入净额":CONVERT.UnitStrToFloat(row[5]) 
                                            ,"主力净流入净占比":CONVERT.UnitStrToFloat(row[6]) 
                                            ,"超大单净流入净额":CONVERT.UnitStrToFloat(row[7]) 
                                            ,"超大单净流入净占比":CONVERT.UnitStrToFloat(row[8])
                                            ,"大单净流入净额":CONVERT.UnitStrToFloat(row[9]) 
                                            ,"大单净流入净占比":CONVERT.UnitStrToFloat(row[10]) 
                                            ,"中单净流入净额":CONVERT.UnitStrToFloat(row[11]) 
                                            ,"中单净流入净占比":CONVERT.UnitStrToFloat(row[12])
                                            ,"小单净流入净额":CONVERT.UnitStrToFloat(row[13]) 
                                            ,"小单净流入净占比":CONVERT.UnitStrToFloat(row[14])  
                                            }
                                    resArr.append(item)
                    post_data = {"taskId":taskId,"keyName":"DPZJLX","jsonReq": json.dumps(data,ensure_ascii=False),"jsonRes": json.dumps(resArr,ensure_ascii=False)}
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
 