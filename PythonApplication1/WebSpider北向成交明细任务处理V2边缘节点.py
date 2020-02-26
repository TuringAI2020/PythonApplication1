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
    serverUrl="http://122.51.159.248/YunStock2Service?keyName=BXCJMX&taskId=%s"%taskId
    #serverUrl="http://127.0.0.1:80/YunStock2Service?keyName=BXCJMX&taskId=%s"%taskId
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
                    jsonStr = spider.LoadWeb(url,"北向成交明细").GetDataFromWeb() 
                    jsonData=json.loads(jsonStr) 

                    if ("Tables" in jsonData and []!=jsonData["Tables"]): 
                        tables = jsonData["Tables"]
                        rows = tables[len(tables)-1]["body"]
                        for row in rows:
                            if 9==len(row):
                                日期Tag = CONVERT.DateToInt(row[0])
                                item={"Code":code
                                      ,"日期":row[0]
                                      ,"日期Tag":CONVERT.DateToInt(row[0])
                                      ,"当日排名":CONVERT.StrToInt(row[2])
                                      ,"收盘价":CONVERT.StrToFloat(row[3])
                                      ,"涨跌幅":CONVERT.UnitStrToFloat(row[4])
                                      ,"沪深股通净买额":CONVERT.UnitStrToFloat(row[5])
                                      ,"沪深股通买入金额":CONVERT.UnitStrToFloat(row[6])
                                      ,"沪深股通卖出金额":CONVERT.UnitStrToFloat(row[7])
                                      ,"沪深股通成交金额":CONVERT.UnitStrToFloat(row[8])}
                                resArr.append(item)

                    post_data={"keyName":"BXCJMX","taskId":taskId,"method":"SaveBXCJMX","jsonReq": json.dumps(data,ensure_ascii=False),"jsonRes": json.dumps(resArr,ensure_ascii=False)}
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
 