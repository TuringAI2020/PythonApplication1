import requests
import json
import time   
import  urllib   
import codecs
import datetime
import io
import random
from pathlib import Path 
import  pandas  as pd
import pymssql
from collections.abc import Iterable

conn = pymssql.connect(server="127.0.0.1:1433",user="sa",password="111qqq!!!",database="WangJunStock")

sql = "SELECT TOP 1000 * FROM  财务主要指标 WHERE Code ='601888'"
df0 = pd.read_sql(sql,conn)
df=pd.DataFrame(df0)
print(df["基本每股收益"].min())
print(df["基本每股收益"].max())
print(df["基本每股收益"].mean())
print(df["基本每股收益"].median())
df = df.sort_values(by="DateTag",ascending=True)
print(df)