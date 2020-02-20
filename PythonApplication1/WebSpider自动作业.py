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
   
from CHECKER import CHECKER 
from RClient import RClient

def StartRZRQTaskProc():
    threadCount=psutil.cpu_count(True)
    path=r"D:\WangJunCode2020\PythonApplication1\PythonApplication1\WebSpider融资融券任务处理V2.py"
    for k in range(threadCount):
        sub=subprocess.Popen("cmd.exe /C python %s"%path,creationflags=subprocess.CREATE_NEW_CONSOLE)
        time.sleep(10)
    pass

def StartRZRQTaskCreate():
    print("StartRZRQTaskCreate")
    threadCount=psutil.cpu_count(True)
    path=r"D:\WangJunCode2020\PythonApplication1\PythonApplication1\WebSpider融资融券任务生成V2.py"
    #_thread.start_new_thread(lambda :os.system("python %s"%path) ,() )
    sub=subprocess.Popen("cmd.exe /C python %s"%path,creationflags=subprocess.CREATE_NEW_CONSOLE)
    time.sleep(20)
    pass

def StartCWFXTaskCreate():
    print("StartCWFXTaskCreate")
    threadCount=psutil.cpu_count(True)
    path=r"D:\WangJunCode2020\PythonApplication1\PythonApplication1\WebSpider新财务分析任务生成V2.py"
    sub=subprocess.Popen("cmd.exe /C python %s"%path,creationflags=subprocess.CREATE_NEW_CONSOLE)
    print(sub)
    time.sleep(20)
    pass
def StartCWFXTaskProc():
    threadCount=psutil.cpu_count(True)
    path=r"D:\WangJunCode2020\PythonApplication1\PythonApplication1\WebSpider新财务分析任务处理V2.py"
    for k in range(threadCount):
        sub=subprocess.Popen("cmd.exe /C python %s"%path,creationflags=subprocess.CREATE_NEW_CONSOLE)
        time.sleep(10)
    pass

def StartZJLXTaskCreate():
    print("StartZJLXTaskCreate")
    threadCount=psutil.cpu_count(True)
    path=r"D:\WangJunCode2020\PythonApplication1\PythonApplication1\WebSpider资金流向任务生成V2.py"
    _thread.start_new_thread(lambda :os.system("python %s"%path) ,() )
    time.sleep(20)
    pass
def StartZJLXTaskProc():
    threadCount=psutil.cpu_count(True)
    path=r"D:\WangJunCode2020\PythonApplication1\PythonApplication1\WebSpider资金流向任务处理V2.py"
    for k in range(threadCount):
        sub=subprocess.Popen("cmd.exe /C python %s"%path,creationflags=subprocess.CREATE_NEW_CONSOLE)
        time.sleep(10)
    pass

def StartBXCGTaskCreate():
    print("StartBXCGTaskCreate")
    threadCount=psutil.cpu_count(True)
    path=r"D:\WangJunCode2020\PythonApplication1\PythonApplication1\WebSpider北向持股明细任务生成V2.py"
    sub=subprocess.Popen("cmd.exe /C python %s"%path,creationflags=subprocess.CREATE_NEW_CONSOLE)
    print(sub)
    time.sleep(20)
    pass
def StartBXCGTaskProc():
    threadCount=psutil.cpu_count(True)
    path=r"D:\WangJunCode2020\PythonApplication1\PythonApplication1\WebSpider北向持股明细任务处理V2.py"
    for k in range(threadCount):
        sub=subprocess.Popen("cmd.exe /C python %s"%path,creationflags=subprocess.CREATE_NEW_CONSOLE)
        time.sleep(10)
    pass
def StartBXCJTaskCreate():
    print("StartBXCJTaskCreate")
    threadCount=psutil.cpu_count(True)
    path=r"D:\WangJunCode2020\PythonApplication1\PythonApplication1\WebSpider北向成交明细任务生成V2.py"
    sub=subprocess.Popen("cmd.exe /C python %s"%path,creationflags=subprocess.CREATE_NEW_CONSOLE)
    print(sub)
    time.sleep(20)
    pass
def StartBXCJTaskProc():
    threadCount=psutil.cpu_count(True)
    path=r"D:\WangJunCode2020\PythonApplication1\PythonApplication1\WebSpider北向成交明细任务处理V2.py"
    for k in range(threadCount):
        sub=subprocess.Popen("cmd.exe /C python %s"%path,creationflags=subprocess.CREATE_NEW_CONSOLE)
        time.sleep(10)
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
print("OK")