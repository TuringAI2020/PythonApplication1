from selenium import webdriver
import time 
from py03 import HtmlConvertor
from RClient import RClient
import json
import time

class ChromeSpider:
    chrome = None
    html = None
    url = None
    def GetDataFromWeb(self):
        res = HtmlConvertor.GetInst().LoadFromString(html=self.html).ConvertToJson()
        return res
        pass

    def SaveDataToRedis(self,callback,redisUrl="127.0.0.1:6379"):
        
        jsonStr = self.GetDataFromWeb()
        data = json.loads(jsonStr)
        data["Uri"] = self.url
        data=callback(data) 
        pageTag=data["PageTag"]
        qName = "PreProcTask:%s"%pageTag 
        RClient.GetInst().QueueEn(qName,data)
        print("已保存%s\t%s"%(data["Name"],data["Code"]))
        pass
    def __init__(self):
        self.chrome = webdriver.Chrome()     # 创建Chrome对象
    def LoadWeb(self,url):
        try:
            self.chrome.get(url)     # get .
            self.chrome.implicitly_wait(10)
            self.html = self.chrome.page_source
            self.url = url
        except BaseException as e:
            print("$s" % e)
            self.url = None
            #self.chrome.quit();
        finally:
            return self
        pass

def callback(input):
     output = input
     title = input["Title"]
     name = title.split('(')[0]
     code = title.split('(')[1].split(')')[0]
     dateTag =time.strftime("%Y%m%d", time.localtime())
     pageTag = title.split('(')[1].split(')')[1].split(" ")[0].strip()
     output["Name"]=name
     output["Code"]=code
     output["DateTag"]=dateTag
     output["PageTag"]=pageTag
     return output
     pass

spider = ChromeSpider()
spider.LoadWeb("http://data.eastmoney.com/zjlx/603501.html").SaveDataToRedis(callback=callback)
print("OK")