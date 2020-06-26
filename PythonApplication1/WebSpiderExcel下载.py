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

def DownloadWebData():
    res0 = requests.get("http://122.51.159.248:5000/YunStockService/List?keyName=ALLCODE")
    print(res0.text)
    allCode = json.loads(res0.text)["data"]
    count = len(allCode)
    index = 0
    while index < count:
        code = allCode[index]["code"]
        try:
            #res1 =
            #requests.get("http://money.finance.sina.com.cn/corp/go.php/vDOWN_BalanceSheet/displaytype/4/stockid/%s/ctrl/all.phtml"
            #% code) #资产负债表
            #time.sleep(random.uniform(5,10))
            #res2 =
            #requests.get("http://money.finance.sina.com.cn/corp/go.php/vDOWN_ProfitStatement/displaytype/4/stockid/%s/ctrl/all.phtml"
            #% code) #利润表
            #time.sleep(random.uniform(5,10))
            #res3 =
            #requests.get("http://money.finance.sina.com.cn/corp/go.php/vDOWN_CashFlow/displaytype/4/stockid/%s/ctrl/all.phtml"
            #% code) #现金流量表
            #time.sleep(random.uniform(5,10))
            path1 = r"%s\资产负债表_%s.xls" % (r"D:\DataSourceStock\资产负债表",code)
            filePath1 = Path(path1)
            e1 = filePath1.exists()

            path2 = r"%s\利润表_%s.xls" % (r"D:\DataSourceStock\利润表",code)
            filePath2 = Path(path2)
            e2 = filePath2.exists()

            path3 = r"%s\现金流量表_%s.xls" % (r"D:\DataSourceStock\现金流量表",code)
            filePath3 = Path(path3)
            e3 = filePath3.exists()

            if True != e1:
                res1 =  requests.get("http://money.finance.sina.com.cn/corp/go.php/vDOWN_BalanceSheet/displaytype/4/stockid/%s/ctrl/all.phtml"% code) #资产负债表
                time.sleep(random.uniform(3,5))
                print("正在下载资产负债表 %s-%s-%s" % (count,index,code))
                f1 = open("%s\资产负债表_%s.xls" %(r"D:\DataSourceStock\资产负债表",code),"wb")
                f1.write(res1.content)
                f1.close()
            else:
                print("资产负债表已存在 %s-%s-%s" % (count,index,code))

            if True != e2:
                res2 =  requests.get("http://money.finance.sina.com.cn/corp/go.php/vDOWN_ProfitStatement/displaytype/4/stockid/%s/ctrl/all.phtml"% code) #利润表
                time.sleep(random.uniform(3,5))
                print("正在下载利润表 %s-%s-%s" % (count,index,code))
                f2 = open("%s\利润表_%s.xls" %(r"D:\DataSourceStock\利润表",code),"wb")
                f2.write(res2.content)
                f2.close()
            else:
                print("利润表已存在 %s-%s-%s" % (count,index,code))

            if True != e3:
                res3 =  requests.get("http://money.finance.sina.com.cn/corp/go.php/vDOWN_CashFlow/displaytype/4/stockid/%s/ctrl/all.phtml"% code) #现金流量表
                time.sleep(random.uniform(3,5))
                print("正在下载现金流量表 %s-%s-%s" % (count,index,code))
                f3 = open("%s\现金流量表_%s.xls" %(r"D:\DataSourceStock\现金流量表",code),"wb")
                f3.write(res3.content)
                f3.close()
            else:
                print("现金流量表已存在 %s-%s-%s" % (count,index,code))
                  
            index+=1 
            
        except BaseException as ex:
            print("%s-%s-%s 异常" % (count,index,code))
            print(ex)
            index-=1
            pass
    pass
DownloadWebData()
print("全部结束")
 