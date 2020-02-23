import os
import random
import time
import sys
import gzip
import urllib
import io  #StringIO模块就是在内存中读写str
import re
import json 
from CHECKER import CHECKER 
from RClient import RClient
from CONVERTOR import CONVERT
import psutil

r=RClient.GetInst() 

def SendSyncNotice(namespace,item):
    if type("") == type(namespace) and 0<len(namespace):
        qName="Stock:Sync:2DB:%s"%namespace
        r.QueueEn(qName,json.dumps(item,ensure_ascii=False))
    pass
