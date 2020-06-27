import requests
import json
import time  
from CHECKER import  CHECKER
import  urllib   
import codecs
import datetime
import io
import random
from pathlib import Path 
import  pandas  as pd
def ReadExcel():
    path = u"D:\DataSourceStock\利润表_000001.csv"
    df1 = pd.read_csv(path,sep='\t')  
    #data=df1.head(100)#默认读取前5行的数据
    #print("获取到所有的值:\n{0}".format(data))#格式化输出
    dict={}
    for col in df1.columns:
        #print(col)
        series = df1[col]
        
        if(series.name == "报表日期"):
            index=0
            dict[index]=series.name
            index=1
            SQL=" CREATE TABLE [利润表] ([Code] NCHAR(6) NOT NULL \r\n,报表日期Tag INT NOT NULL"
            for row in series:
                arr=row.split('、')
                arr=arr[len(arr)-1].split(':')
                arr=arr[len(arr)-1].split('：')
                row=arr[len(arr)-1]
                dict[index]=row
                if row!="单位":
                    SQL="%s,[%s] [numeric](18, 2)  NULL \r\n"%(SQL,row)
                index+=1
            SQL="%s)"%SQL
            print(SQL)
            print("\r\n\r\n\r\n\r\n")
            pass
        else:
            item={}
            index=0
            item[dict[index]]=series.name
            index=1
            for row in series: 
                item[dict[index]]=row
                index+=1
            print(item)
            print("\r\n\r\n\r\n\r\n")
            pass
        #print(series)
        #print(series[1])
    #print(df1["19961231"])
    pass
ReadExcel()
print("全部结束")
 