import requests
import json
import time
#from selenium import webdriver
#from selenium.webdriver.support.select import Select
#from selenium.webdriver.chrome.options import Options
from ChromeSpider import ChromeSpider
from CONVERTOR import CONVERT

spider = ChromeSpider() 
def ProcWebData():
    taskId="Task1"
    serverUrl="http://122.51.159.248/YunStock2Service?keyName=ZJLX&taskId=%s"%taskId
    #serverUrl="http://127.0.0.1:80/YunStock2Service?keyName=ZJLX&taskId=%s"%taskId
    while True:
        try:
            res = requests.get(serverUrl)
            print("接收 %s \r\n --------\r\n"%res.text)
            res = json.loads(res.text)
            if(res["success"]== True ):
                data = res["data"]
                if 10<=len(data):
                    data = json.loads(data)
                    code=data["Code"]
                    url=data["Url"]
                    resArr=[]
                    jsonStr = spider.LoadWeb(url,"资金流向").GetDataFromWeb() 
                    jsonData=json.loads(jsonStr) 

                    if ("Tables" in jsonData and []!=jsonData["Tables"]): 
                        tables = jsonData["Tables"]
                        rows = tables[len(tables)-1]["body"]
                        for row in rows:
                            if 13==len(row):
                                日期Tag = CONVERT.DateToInt(row[0])
                                item={"Code":code
                                      ,"日期":row[0]
                                      ,"日期Tag":日期Tag
                                      ,"收盘价":CONVERT.StrToFloat(row[1])
                                      ,"涨跌幅":CONVERT.UnitStrToFloat(row[2])
                                      ,"主力净流入净额":CONVERT.UnitStrToFloat(row[3])
                                      ,"主力净流入净占比":CONVERT.UnitStrToFloat(row[4])
                                      ,"超大单净流入净额":CONVERT.UnitStrToFloat(row[5])
                                      ,"超大单净流入净占比":CONVERT.UnitStrToFloat(row[6])
                                      ,"大单净流入净额":CONVERT.UnitStrToFloat(row[7])
                                      ,"大单净流入净占比":CONVERT.UnitStrToFloat(row[8])
                                      ,"中单净流入净额":CONVERT.UnitStrToFloat(row[9])
                                      ,"中单净流入净占比":CONVERT.UnitStrToFloat(row[10])
                                      ,"小单净流入净额":CONVERT.UnitStrToFloat(row[11])
                                      ,"小单净流入净占比":CONVERT.UnitStrToFloat(row[12])
                                      }
                                resArr.append(item)

                    post_data={"keyName":"ZJLX","taskId":taskId,"method":"SaveProcData","jsonReq": json.dumps(data,ensure_ascii=False),"jsonRes": json.dumps(resArr,ensure_ascii=False)}
                    res2 = requests.post(serverUrl,data=post_data)
                    print("POST %s \r\n RES %s \r\n --------- \r\n"%(post_data,res2.text))
 
            else:
                time.sleep(5)
        except BaseException as e:
            print(" 异常 %s "%e)
            time.sleep(20)
    pass
ProcWebData()
spider.Quit()
print("全部结束")
 