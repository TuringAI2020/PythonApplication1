from selenium import webdriver
import time 
from py03 import HtmlConvertor
from RClient import RClient
 
class ChromeSpider:
    chrome=None
    html=None
    def GetDataFromWeb(self):
        res = HtmlConvertor.GetInst().LoadFromString(html=self.html).ConvertToJson()
        return res
        pass

    def SaveDataToRedis(self,redisUrl="127.0.0.1:6379"):
        qName="测试";
        data = self.GetDataFromWeb()
        RClient.GetInst().QueueEn(qName,data)
        pass
    def __init__(self):
        self.chrome = webdriver.Chrome()     # 创建Chrome对象
    def LoadWeb(self,url):
        try:
            self.chrome.get(url)     # get方式访问百度.
            self.chrome.implicitly_wait(10)
            self.html = self.chrome.page_source
        except BaseException as e:
            print("$s"%e)
        finally:
            return self
        pass

spider = ChromeSpider()
spider.LoadWeb("http://data.eastmoney.com/stockdata/002174.html").SaveDataToRedis();
print("OK")