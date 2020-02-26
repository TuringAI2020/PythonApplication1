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
    taskId="Task0"
    serverUrl="http://122.51.159.248/YunStock2Service?keyName=RZRQ&taskId=%s"%taskId
    #serverUrl="http://127.0.0.1:80/YunStock2Service?keyName=RZRQ&taskId=%s"%taskId
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
                    jsonStr = spider.LoadWeb(url,"融资融券").GetDataFromWeb() 
                    jsonData=json.loads(jsonStr) 

                    if ("Tables" in jsonData and []!=jsonData["Tables"]): 
                        tables = jsonData["Tables"]
                        rows = tables[len(tables)-1]["body"]
                        for row in rows:
                            if 15==len(row):
                                交易日期Tag = CONVERT.DateToInt(row[0])
                                item={"Code":code
                                        ,"交易日期":row[0]
                                        ,"交易日期Tag":交易日期Tag
                                        ,"收盘价":CONVERT.StrToFloat(row[1])
                                        ,"涨跌幅":CONVERT.UnitStrToFloat(row[2])
                                        ,"融资余额":CONVERT.UnitStrToFloat(row[3])
                                        ,"融资余额占流通市值比":CONVERT.UnitStrToFloat(row[4])
                                        ,"融资买入额":CONVERT.UnitStrToFloat(row[5])
                                        ,"融资偿还额":CONVERT.UnitStrToFloat(row[6])
                                        ,"融资净买入":CONVERT.UnitStrToFloat(row[7])
                                        ,"融券余额":CONVERT.UnitStrToFloat(row[8])
                                        ,"融券余量":CONVERT.UnitStrToFloat(row[9])
                                        ,"融券卖出量":CONVERT.UnitStrToFloat(row[10])
                                        ,"融券偿还量":CONVERT.UnitStrToFloat(row[11])
                                        ,"融券净卖出":CONVERT.UnitStrToFloat(row[12])
                                        ,"融资融券余额":CONVERT.UnitStrToFloat(row[13])
                                        ,"融资融券余额差值":CONVERT.UnitStrToFloat(row[14])
                                        }
                                resArr.append(item)

                    post_data={"keyName":"RZRQ","taskId":taskId,"method":"SaveProcData","jsonReq": json.dumps(data,ensure_ascii=False),"jsonRes": json.dumps(resArr,ensure_ascii=False)}
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
 