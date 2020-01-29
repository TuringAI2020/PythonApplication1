from selenium import webdriver
import time 
from py03 import HtmlConvertor
from RClient import RClient
import json
import time
from selenium.webdriver.chrome.options import Options

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
        if None != data:
            pageTag=data["PageTag"]
            qName = "PreProcTask:%s"%pageTag 
            RClient.GetInst().QueueEn(qName,data)
            print("已保存%s\t%s"%(data["Name"],data["Code"]))
        else:
            print("下载失败%s"%self.url)
            time.sleep(60)
        pass
    def __init__(self):
        chrome_opt = Options()      # 创建参数设置对象.
        chrome_opt.add_argument('--headless')   # 无界面化.
        chrome_opt.add_argument('--disable-gpu')    # 配合上面的无界面化.
        chrome_opt.add_argument('--window-size=400,1080')   # 设置窗口大小, 窗口大小会有影响.
        self.chrome = webdriver.Chrome(chrome_options=chrome_opt)     # 创建Chrome对象
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
            #self.chrome.close();
            return self
        pass



#spider = ChromeSpider()
#spider.LoadWeb("http://data.eastmoney.com/zjlx/603501.html").SaveDataToRedis(callback=callback)
#print("OK")