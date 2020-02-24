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
    serverUrl="http://122.51.159.248/YunStockService?taskId=%s"%taskId
    #serverUrl="http://127.0.0.1:5000/YunStockService?taskId=%s"%taskId
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
                    jsonStr = spider.LoadWeb(url,"北向持股明细").GetDataFromWeb() 
                    jsonData=json.loads(jsonStr)
                    if "Tables" in jsonData: 
                        tables = jsonData["Tables"]
                        if 0<len(tables):
                            rows=tables[len(tables)-1]["body"]
                            for row in rows:
                                if 12 == len(row): 
                                    持股日期Tag=CONVERT.DateToInt(row[0])
                                    item={
                                        "Code":code
                                            ,"持股日期":row[0]
                                            ,"持股日期Tag":持股日期Tag
                                            ,"股票代码":row[1]
                                            ,"股票简称":row[2]
                                            ,"当日收盘价":CONVERT.StrToFloat(row[3])
                                            ,"当日涨跌幅":CONVERT.StrToFloat(row[4])
                                            ,"机构名称":row[5]
                                            ,"持股数量":CONVERT.UnitStrToFloat(row[6])
                                            ,"持股市值":CONVERT.UnitStrToFloat(row[7])
                                            ,"持股数量占A股百分比":CONVERT.StrToFloat(row[8])
                                            ,"持股市值变化1日":CONVERT.UnitStrToFloat(row[9])
                                            ,"持股市值变化5日":CONVERT.UnitStrToFloat(row[10])
                                            ,"持股市值变化10日":CONVERT.UnitStrToFloat(row[11])
                                            }
                                    resArr.append(item)
                    post_data={"taskId":taskId,"method":"SaveBXCGMX","jsonReq": json.dumps(data,ensure_ascii=False),"jsonRes": json.dumps(resArr,ensure_ascii=False)}
                    res2 = requests.post(serverUrl,data=post_data)
                    print("POST %s \r\n RES %s \r\n --------- \r\n"%(post_data,res2.text))
            else:
                time.sleep(3)
        except BaseException as e:
            print(" 异常 %s "%e)
            time.sleep(20)
    pass
ProcWebData()
spider.Quit()
print("全部结束")
 