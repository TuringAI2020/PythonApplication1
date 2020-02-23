import os
import random
import time
import sys
import gzip
import urllib
import urllib.request
import io  #StringIO模块就是在内存中读写str
import re
import json
import _thread
import psutil
import subprocess
import datetime
import sched
   
from CHECKER import CHECKER 
from RClient import RClient
root="D:\\WangJunCode2020\\PythonApplication1\\PythonApplication1\\"
def StartRZRQTaskProc():
    threadCount=psutil.cpu_count(True)
    path=r"%s\WebSpider融资融券任务处理V2.py"%root
    for k in range(threadCount):
        sub=subprocess.Popen("cmd.exe /C python %s"%path,creationflags=subprocess.CREATE_NEW_CONSOLE)
        time.sleep(10)
    pass

def StartRZRQTaskCreate():
    print("StartRZRQTaskCreate")
    threadCount=psutil.cpu_count(True)
    path=r"%s\WebSpider融资融券任务生成V2.py"%root
    sub=subprocess.Popen("cmd.exe /C python %s"%path,creationflags=subprocess.CREATE_NEW_CONSOLE)
    time.sleep(20)
    pass
def StartRZRQTask():
    StartRZRQTaskCreate()
    StartRZRQTaskProc()
    pass

def StartCWFXTaskCreate():
    print("StartCWFXTaskCreate")
    threadCount=psutil.cpu_count(True)
    path=r"%s\WebSpider新财务分析任务生成V2.py"%root 
    sub=subprocess.Popen("cmd.exe /C python %s"%path,creationflags=subprocess.CREATE_NEW_CONSOLE) 
    time.sleep(20)
    pass
def StartCWFXTaskProc():
    threadCount=psutil.cpu_count(True) 
    path=r"%s\WebSpider新财务分析任务处理V2.py"%root 
    for k in range(threadCount):
        sub=subprocess.Popen("cmd.exe /C python %s"%path,creationflags=subprocess.CREATE_NEW_CONSOLE)
        time.sleep(10)
    pass

def StartCWFXTask():
    StartCWFXTaskCreate()
    StartCWFXTaskProc()
    pass

def StartZJLXTaskCreate():
    print("StartZJLXTaskCreate")
    threadCount=psutil.cpu_count(True) 
    path=r"%s\WebSpider资金流向任务生成V2.py"%root 
    _thread.start_new_thread(lambda :os.system("python %s"%path) ,() )
    time.sleep(20)
    pass
def StartZJLXTaskProc():
    threadCount=psutil.cpu_count(True)
    path=r"%s\WebSpider资金流向任务处理V2.py"%root  
    for k in range(threadCount):
        sub=subprocess.Popen("cmd.exe /C python %s"%path,creationflags=subprocess.CREATE_NEW_CONSOLE)
        time.sleep(10)
    pass

def StartZJLXTask():
    StartZJLXTaskCreate()
    StartZJLXTaskProc()
    pass

def StartBXCGTaskCreate():
    print("StartBXCGTaskCreate")
    threadCount=psutil.cpu_count(True)
    path=r"%s\WebSpider北向持股明细任务生成V2.py"%root
    sub=subprocess.Popen("cmd.exe /C python %s"%path,creationflags=subprocess.CREATE_NEW_CONSOLE)
    print(sub)
    time.sleep(20)
    pass
def StartBXCGTaskProc():
    threadCount=psutil.cpu_count(True)
    path=r"%s\WebSpider北向持股明细任务处理V2.py"%root
    for k in range(threadCount):
        sub=subprocess.Popen("cmd.exe /C python %s"%path,creationflags=subprocess.CREATE_NEW_CONSOLE)
        time.sleep(10)
    pass

def StartBXCGTask():
    StartBXCGTaskCreate()
    StartBXCGTaskProc()
    pass

def StartBXCJTaskCreate():
    print("StartBXCJTaskCreate")
    threadCount=psutil.cpu_count(True)
    path=r"%s\WebSpider北向成交明细任务生成V2.py"%root     
    sub=subprocess.Popen("cmd.exe /C python %s"%path,creationflags=subprocess.CREATE_NEW_CONSOLE)
    print(sub)
    time.sleep(20)
    pass
def StartBXCJTaskProc():
    threadCount=psutil.cpu_count(True)
    path=r"%s\WebSpider北向成交明细任务处理V2.py"%root     
    for k in range(threadCount):
        sub=subprocess.Popen("cmd.exe /C python %s"%path,creationflags=subprocess.CREATE_NEW_CONSOLE)
        time.sleep(10)
    pass

def StartBXCJTask():
    StartBXCJTaskCreate()
    StartBXCJTaskProc()
    pass
#StartRZRQTaskCreate()
#StartRZRQTaskProc()
#StartCWFXTaskCreate()
#StartCWFXTaskProc()
#StartZJLXTaskCreate()
#StartZJLXTaskProc()
#StartBXCGTaskCreate()
#StartBXCGTaskProc()
#StartBXCJTaskCreate()
#StartBXCJTaskProc()

def Test1(data,data2):
    print("Test1 %s %s"%(data,data2))
    time.sleep(data2)
    pass

startTime = datetime.datetime.now()
lastCheckTime = datetime.datetime.now() 
sc = sched.scheduler(time.time,time.sleep)
r=RClient.GetInst()
jobNamespace="Stock:Task:Job" 

def InitialJob():
    r.DeleteKeys(jobNamespace)
    today = datetime.date.today()
    r.DictSave(jobNamespace,"资金流向任务"
               ,{"Code":"资金流向任务"
               ,"Name":"资金流向任务"
               ,"StartTime":datetime.date.today().strftime("%Y-%m-%d 15:10:00") #每天定时执行
               ,"Status":"Pending"})
    r.DictSave(jobNamespace,"融资融券任务"
               ,{"Code":"融资融券任务"
               ,"Name":"融资融券任务"
               ,"StartTime":datetime.date.today().strftime("%Y-%m-%d 17:10:00") #每天定时执行
               ,"Status":"Pending"})
    r.DictSave(jobNamespace,"财务主要指标任务"
               ,{"Code":"财务主要指标任务"
               ,"Name":"财务主要指标任务"
               ,"StartTime":datetime.date.today().strftime("%Y-%m-%d 19:10:00") #每天定时执行
               ,"Status":"Pending"})
    r.DictSave(jobNamespace,"核心题材任务"
               ,{"Code":"核心题材任务"
               ,"Name":"核心题材任务"
               ,"StartTime":datetime.date.today().strftime("%Y-%m-%d 19:10:00") #每天定时执行
               ,"Status":"Pending"})
    r.DictSave(jobNamespace,"概念任务"
               ,{"Code":"概念任务"
               ,"Name":"概念任务"
               ,"StartTime":datetime.date.today().strftime("%Y-%m-%d 19:10:00") #每天定时执行
               ,"Status":"Pending"})
    r.DictSave(jobNamespace,"北向成交明细任务"
               ,{"Code":"北向成交明细任务"
               ,"Name":"北向成交明细任务"
               ,"StartTime":datetime.date.today().strftime("%Y-%m-%d 21:10:00") #每天定时执行
               ,"Status":"Pending"})
    r.DictSave(jobNamespace,"北向持股明细任务"
               ,{"Code":"北向持股明细任务"
               ,"Name":"北向持股明细任务"
               ,"StartTime":datetime.date.today().strftime("%Y-%m-%d 16:10:00") #每天定时执行
               ,"Status":"Pending"})
    r.DictSave(jobNamespace,"东方财富网-滚动新闻采集"
               ,{"Code":"东方财富网-滚动新闻采集"
               ,"Name":"东方财富网-滚动新闻采集"
               ,"StartTime":(datetime.datetime.now()+datetime.timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S")# 15分钟抓取一次
               ,"Status":"Pending"})
    r.DictSave(jobNamespace,"中国政府网-要闻采集"
               ,{"Code":"中国政府网-要闻采集"
               ,"Name":"中国政府网-要闻采集"
               ,"StartTime":(datetime.datetime.now()+datetime.timedelta(minutes=60)).strftime("%Y-%m-%d %H:%M:%S")# 15分钟抓取一次
               ,"Status":"Pending"})
    
    pass

def ProcJob(dictName,key,val,pageIndex,pageCount,pageSize,curIndex,total):
    print("%s"%key)
    currentTime = datetime.datetime.now() 
    val = json.loads(val)
    code= val["Code"]
    val["Status"]="Running"
    val["StartTime"]=datetime.datetime.strptime(val["StartTime"],"%Y-%m-%d %H:%M:%S")
    val["CheckTime"]=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if "资金流向任务" == code and val["StartTime"]<=currentTime and currentTime.weekday()<6:
        val["StartTime"]=(val["StartTime"]+datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        StartZJLXTask()
        r.DictSave(dictName,key ,val)
    elif "融资融券任务" == code and val["StartTime"]<=currentTime and currentTime.weekday()<6:
        val["StartTime"]=(val["StartTime"]+datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        StartRZRQTask()
        r.DictSave(dictName,key ,val)
    elif "财务主要指标任务" == code and val["StartTime"]<=currentTime and currentTime.weekday()<6:
        val["StartTime"]=(val["StartTime"]+datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        StartCWFXTask()
        r.DictSave(dictName,key ,val)
    elif "核心题材任务" == code and val["StartTime"]<=currentTime and currentTime.weekday()==6:
        val["StartTime"]=(val["StartTime"]+datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        print("处理 %s"%key)
        r.DictSave(dictName,key ,val)
    elif "概念任务" == code and val["StartTime"]<=currentTime and 6==currentTime.weekday():
        val["StartTime"]=(val["StartTime"]+datetime.timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S")
        print("处理 %s"%key)
        r.DictSave(dictName,key ,val)
    elif "北向成交明细任务" == code and val["StartTime"]<=currentTime and currentTime.weekday()<=6:
        val["StartTime"]=(val["StartTime"]+datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        StartBXCJTask()
        r.DictSave(dictName,key ,val)
    elif "北向持股明细任务" == code and val["StartTime"]<=currentTime and currentTime.weekday()<=6:
        val["StartTime"]=(val["StartTime"]+datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        StartBXCGTask()
        r.DictSave(dictName,key ,val)
    elif "东方财富网-滚动新闻采集" == code and val["StartTime"]<=currentTime:
        val["StartTime"]=(val["StartTime"]+datetime.timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S")
        print("处理 %s"%key)
        r.DictSave(dictName,key ,val)
    elif "中国政府网-要闻采集" == code and val["StartTime"]<=currentTime:
        val["StartTime"]=(val["StartTime"]+datetime.timedelta(minutes=60)).strftime("%Y-%m-%d %H:%M:%S")
        print("处理 %s"%key)
        r.DictSave(dictName,key ,val)
    time.sleep(2)
    pass

def JobRunner():
    while True:
        lastCheckTime =  datetime.datetime.now()
        r.TraverseDict(jobNamespace,ProcJob)
        print("循环结束 %s"%lastCheckTime)
        time.sleep(100)
    pass

JobRunner()
#InitialJob()
print("自动作业全部结束")