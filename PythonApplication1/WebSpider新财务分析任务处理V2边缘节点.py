import requests
import json
import time
#from selenium import webdriver
#from selenium.webdriver.support.select import Select
#from selenium.webdriver.chrome.options import Options
from ChromeSpider import ChromeSpider
from CONVERTOR import CONVERT
from CHECKER import CHECKER
spider = ChromeSpider() 

def CreateEmptyItem(table):
    rows = table["body"]
    item = {}
    for row in rows:
         item[row[0].strip()] = ""
    return item

def CreateEmptyItemList(table):
    rows = table["body"]
    itemCount = 0
    arr = []
    if(0 < len(rows)):
        itemCount = len(rows[0]) - 1
    while 0 < itemCount:
        item = CreateEmptyItem(table)
        arr.append(item)
        itemCount-=1
    return arr

def FillItemList(table):
     arr = CreateEmptyItemList(table)
     rows = table["body"]
     
     for row in rows:
         key = row[0]
         rowIndex = 1
         while rowIndex < len(arr):
             if True != CHECKER.IsDate(row[rowIndex]): 
                arr[rowIndex - 1][key] = CONVERT.UnitStrToFloat(row[rowIndex],unit=None)
             else:
                 if 8 == len(row[rowIndex]) and int(row[rowIndex][0])<3:
                     row[rowIndex] = "20" + row[rowIndex] 
                 elif 8 == len(row[rowIndex]) and 3<=int(row[rowIndex][0]):
                     row[rowIndex] = "19" + row[rowIndex] 
                 arr[rowIndex - 1][key + "Tag"] = CONVERT.DateToInt(row[rowIndex])
                 arr[rowIndex - 1][key] = row[rowIndex] 
                 arr[rowIndex - 1]["DateTag"] = CONVERT.DateToInt(row[rowIndex])
                
             rowIndex+=1
     return arr  

def ProcWebData():
    taskId="Task1"
    serverUrl="http://122.51.159.248/YunStock2Service?keyName=CWFX&taskId=%s"%taskId
    #serverUrl="http://127.0.0.1:80/YunStock2Service?keyName=CWFX&taskId=%s"%taskId
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
                    jsonStr = spider.LoadWeb(url,"财务分析").GetDataFromWeb() 
                    jsonData=json.loads(jsonStr) 
                    财务主要指标 = jsonData["Tables"][0]
                    财务主要指标 = FillItemList(财务主要指标)
                    财务主要指标 = list(filter(lambda x:"每股指标Tag" in x,财务主要指标))
                    for item in  财务主要指标:
                        item["Code"]=code
                        resArr.append(item)
                    post_data={"keyName":"CWFX","taskId":taskId,"method":"SaveProcData","jsonReq": json.dumps(data,ensure_ascii=False),"jsonRes": json.dumps(resArr,ensure_ascii=False)}
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
 