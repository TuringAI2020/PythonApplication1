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
  
def 资金流向任务创建(): 
    #serverUrl="http://122.51.159.248/YunStockTaskService"
    serverUrl="http://127.0.0.1:80/YunStockTaskService"
    post_data={"method":"CreateTask资金流向",  "jsonReq": json.dumps({},ensure_ascii=False),"jsonRes": json.dumps({},ensure_ascii=False)}
    res2 = requests.post(serverUrl,data=post_data)
    print("POST %s \r\n RES %s \r\n --------- \r\n"%(post_data,res2.text))
    print("OK %s"%serverUrl)


     
资金流向任务创建() 
