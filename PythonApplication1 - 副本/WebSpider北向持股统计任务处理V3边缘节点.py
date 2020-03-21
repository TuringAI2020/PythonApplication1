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
    serverUrl="http://122.51.159.248:5000/YunStock2Service?keyName=BXCGTJ&taskId=%s" % taskId
    #serverUrl = "http://127.0.0.1:5000/YunStock2Service?keyName=BXCGTJ&taskId=%s" % taskId
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
                    jgCode = params["jgCode"][0]

                    resArr = []
                    jsonStr = spider.LoadWeb(url,"北向持股统计").GetDataFromWeb() 
                    jsonData = json.loads(jsonStr)
                    if "Tables" in jsonData: 
                        tables = jsonData["Tables"]
                        if 0 < len(tables):
                            rows = tables[len(tables) - 1]["body"]
                            for row in rows:
                                if 8 == len(row): 
                                    持股日期Tag = CONVERT.DateToInt(row[0])
                                    item = { 
                                             "jgCode":jgCode
                                            ,"持股日期":row[0]
                                            ,"持股日期Tag":持股日期Tag
                                            ,"机构名称":row[1] 
                                            ,"持股只数":CONVERT.StrToInt(row[3])
                                            ,"持股市值":CONVERT.UnitStrToFloat(row[4])
                                            ,"持股市值变化1日":CONVERT.UnitStrToFloat(row[5])
                                            ,"持股市值变化5日":CONVERT.UnitStrToFloat(row[6])
                                            ,"持股市值变化10日":CONVERT.UnitStrToFloat(row[7])
                                            }
                                    resArr.append(item)
                    post_data = {"taskId":taskId,"keyName":"BXCGTJ","jsonReq": json.dumps(data,ensure_ascii=False),"jsonRes": json.dumps(resArr,ensure_ascii=False)}
                    res2 = requests.post(serverUrl,data=post_data)
                    print("POST %s \r\n RES %s \r\n --------- \r\n" % (post_data,res2.text))

                    if "Links" in jsonData: 
                        links = jsonData["Links"]
                        links = list(filter(lambda x:CHECKER.StartWith(x["Href"],"/hsgtcg/InstitutionHdDetail.aspx\?jgCode=") and x["Text"] == "详细",links))
                        links = list(map(lambda x:"http://data.eastmoney.com%s"%x["Href"],links))
                        items = []
                        for link in  links:
                            params = urllib.parse.parse_qs(urllib.parse.urlparse(link).query)
                            date = params["date"][0]
                            dateTag = CONVERT.DateToInt(date)
                            jgCode = params["jgCode"][0]
                            jgName = urllib.parse.unquote(params["jgName"][0].replace('%u', '\\u').encode('utf-8').decode('unicode-escape')).strip()
                            item = {"DateTag":dateTag,"Date":date,"jgCode":jgCode,"jgName":jgName,"Url":link,"RetryCount":3}
                            items.append(item)
                        post_data2 = {"keyName":"BXCGMXURLTASK","jsonReq": json.dumps(data,ensure_ascii=False),"jsonRes": json.dumps(items,ensure_ascii=False)}
                        res3 = requests.post(serverUrl,data=post_data2)
                        print("POST %s \r\n RES %s \r\n --------- \r\n" % (post_data2,res3.text))
                        count+=1
                        print("已处理 %s"%count)
            else:
                time.sleep(3)
        except BaseException as e:
            print(" 异常 %s " % e)
            time.sleep(20)
    pass
ProcWebData()
spider.Quit()
print("全部结束")
 