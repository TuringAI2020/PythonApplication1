import os
import random
import time
import sys 
import io  #StringIO模块就是在内存中读写str
import re
import json
import requests
 
from CHECKER import CHECKER 
from urllib import parse
  
def 北向持股统计任务创建(): 
    #serverUrl="http://122.51.159.248/YunStockTaskService?method=CreateTask北向持股统计"
    serverUrl="http://127.0.0.1:80/YunStockTaskService?method=CreateTask北向持股统计"
    post_data={"method":"CreateTask北向持股统计",  "jsonReq": json.dumps({},ensure_ascii=False),"jsonRes": json.dumps({},ensure_ascii=False)}
    res2 = requests.post(serverUrl,data=post_data)
    print("POST %s \r\n RES %s \r\n --------- \r\n"%(post_data,res2.text))
     


     
北向持股统计任务创建() 
print("OK")