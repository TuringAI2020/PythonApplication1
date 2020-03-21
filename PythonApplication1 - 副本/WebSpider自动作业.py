import os
import random
import time
import sys 
import io  #StringIO模块就是在内存中读写str
import re
import json
import datetime
import requests


def 北向成交明细任务创建(): 
    serverUrl="http://122.51.159.248/YunStockTaskService?method=CreateTask北向成交明细"
    #serverUrl="http://127.0.0.1:80/YunStockTaskService?method=CreateTask北向成交明细"
    post_data={"method":"CreateTask北向成交明细",  "jsonReq": json.dumps({},ensure_ascii=False),"jsonRes": json.dumps({},ensure_ascii=False)}
    res2 = requests.post(serverUrl,data=post_data)
    print("POST %s \r\n RES %s \r\n --------- \r\n"%(post_data,res2.text))
    print("OK %s"%serverUrl)

def 北向持股统计任务创建(): 
    serverUrl="http://122.51.159.248/YunStockTaskService?method=CreateTask北向持股统计"
    #serverUrl="http://127.0.0.1:80/YunStockTaskService?method=CreateTask北向持股统计"
    post_data={"method":"CreateTask北向持股统计",  "jsonReq": json.dumps({},ensure_ascii=False),"jsonRes": json.dumps({},ensure_ascii=False)}
    res2 = requests.post(serverUrl,data=post_data)
    print("POST %s \r\n RES %s \r\n --------- \r\n"%(post_data,res2.text))
    print("OK %s"%serverUrl)

def 融资融券任务创建(): 
    serverUrl="http://122.51.159.248/YunStockTaskService"
    #serverUrl="http://127.0.0.1:80/YunStockTaskService"
    post_data={"method":"CreateTask融资融券",  "jsonReq": json.dumps({},ensure_ascii=False),"jsonRes": json.dumps({},ensure_ascii=False)}
    res2 = requests.post(serverUrl,data=post_data)
    print("POST %s \r\n RES %s \r\n --------- \r\n"%(post_data,res2.text))
    print("OK %s"%serverUrl)

def 资金流向任务创建(): 
    serverUrl="http://122.51.159.248/YunStockTaskService"
    #serverUrl="http://127.0.0.1:80/YunStockTaskService"
    post_data={"method":"CreateTask资金流向",  "jsonReq": json.dumps({},ensure_ascii=False),"jsonRes": json.dumps({},ensure_ascii=False)}
    res2 = requests.post(serverUrl,data=post_data)
    print("POST %s \r\n RES %s \r\n --------- \r\n"%(post_data,res2.text))
    print("OK %s"%serverUrl)

def 财务分析任务创建(): 
    serverUrl="http://122.51.159.248/YunStockTaskService"
    #serverUrl="http://127.0.0.1:80/YunStockTaskService"
    post_data={"method":"CreateTask财务分析",  "jsonReq": json.dumps({},ensure_ascii=False),"jsonRes": json.dumps({},ensure_ascii=False)}
    res2 = requests.post(serverUrl,data=post_data)
    print("POST %s \r\n RES %s \r\n --------- \r\n"%(post_data,res2.text))
    print("OK %s"%serverUrl)

today = datetime.datetime.today()

taskStatus = {
                "北向统计及持股":datetime.datetime(today.year,today.month,today.day,4,0,0)
                ,"北向成交":datetime.datetime(today.year,today.month,today.day,2,0,0) 
                ,"融资融券":datetime.datetime(today.year,today.month,today.day,5,0,0)
                ,"资金流向":datetime.datetime(today.year,today.month,today.day,16,0,0)
                ,"财务分析":datetime.datetime(today.year,today.month,today.day,18,0,0)
              }

def TaskRunner():
    while True:
        currentTime = datetime.datetime.now()

        if taskStatus["北向统计及持股"]<=currentTime:
            print("准备启动北向统计及持股任务 %s %s"%(taskStatus["北向统计及持股"],currentTime))
            taskStatus["北向统计及持股"]+=datetime.timedelta(days=1)
            print("下次北向统计及持股任务启动时间 %s"% taskStatus["北向统计及持股"])
            北向持股统计任务创建()

 
        if taskStatus["北向成交"]<=currentTime:
            print("准备启动北向成交任务 %s %s"%(taskStatus["北向成交"],currentTime))
            taskStatus["北向成交"]+=datetime.timedelta(days=1)
            print("下次北向成交任务启动时间 %s"% taskStatus["北向成交"])
            北向成交明细任务创建()  

        if taskStatus["融资融券"]<=currentTime:
            print("准备启动融资融券任务 %s %s"%(taskStatus["融资融券"],currentTime))
            taskStatus["融资融券"]+=datetime.timedelta(days=1)
            print("下次融资融券任务启动时间 %s"% taskStatus["融资融券"])
            融资融券任务创建()

        if taskStatus["资金流向"]<=currentTime:
            print("准备启动资金流向任务 %s %s"%(taskStatus["资金流向"],currentTime))
            taskStatus["资金流向"]+=datetime.timedelta(days=1)
            print("下次资金流向任务启动时间 %s"% taskStatus["资金流向"])
            资金流向任务创建()

        if taskStatus["财务分析"]<=currentTime:
            print("准备启动财务分析任务 %s %s"%(taskStatus["财务分析"],currentTime))
            taskStatus["财务分析"]+=datetime.timedelta(days=1)
            print("下次财务分析启动时间 %s"% taskStatus["财务分析"])
            财务分析任务创建()

        print("任务检查 当前时间 %s"%currentTime)
        for key in taskStatus:
            print("任务计划 %s\t%s"%(key,taskStatus[key]))
        time.sleep(10)


    pass

TaskRunner()