import os
import random
import time
import sys
import gzip 
import io  #StringIO模块就是在内存中读写str
import re
import json
import datetime
   
import requests

def GetStockIndexData(url):
    res = requests.get(url)
    jsonRes =json.loads(res.text)
    if jsonRes["code"]==200:
       jsondata=jsonRes["data"]
       dataList=[]
       for listItem in jsondata:
           item={
                "indexCode":listItem["indexCode"],
                "indexName":listItem["indexName"],
                "timestamp":listItem["data"][0][0],
                "current":listItem["data"][0][1],
                "chg":listItem["data"][0][6],
                "percent":listItem["data"][0][7],
                }
           dataList.append(item)
       return dataList
    return None

def GetStockIndexList():
    data1 = GetStockIndexData("http://hq.cnindex.com.cn/market/market/getLatestRealTimeDataByIndexCodes?indexCodes=399001%3B399330%3B399006%3B399088%3B399005%3B399317%3B399311%3B399303%3B980003")
    data2 = GetStockIndexData("http://hq.cnindex.com.cn/market/market/getLatestRealTimeDataByIndexCodes?indexCodes=000001%3B000016%3B399300%3B399905%3B399550%3B989001")
    data3 = GetStockIndexData("http://hq.cnindex.com.cn/market/market/getLatestRealTimeDataByIndexCodes?indexCodes=CNG10001%3B002001%3B002002%3B002003%3B002008%3B005001")
    data4 = GetStockIndexData("http://hq.cnindex.com.cn/market/market/getLatestRealTimeDataByIndexCodes?indexCodes=001001%3B001002%3B001004%3B001007")
    dataList=[]
    dataList.extend(data1)
    dataList.extend(data2)
    dataList.extend(data3)
    dataList.extend(data4)
    print(dataList)
    postData={"keyName":"STOCKINDEX","jsonRes":json.dumps(dataList,ensure_ascii=False)}
    res = requests.post("http://122.51.159.248:5000/YunStock2Service",postData)
    print("%s\t%s"%(datetime.datetime.now(),res.text))
    pass

def Run():
    while True:
        now = datetime.datetime.now()
        today=now.date()
        GetStockIndexList()
        print("股票指数更新时间 %s"%now)
        if now.hour>=9 and now.hour<=15 and today.weekday()<5:
            time.sleep(10)
        else:
            time.sleep(300)

Run()