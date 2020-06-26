from selenium import webdriver
import time 
from HtmlConvertor import HtmlConvertor
from RClient import RClient
import json
import time
from selenium.webdriver.chrome.options import Options

class ChromeSpider2:
    chrome = None
    html = None
    url = None
    args=None
    def GetDataFromWeb(self):
        res = HtmlConvertor.GetInst().LoadFromString(html=self.html).ConvertToJson()
        return res
        pass

    def __init__(self):
        chrome_opt = Options()      # 创建参数设置对象.
        #chrome_opt.add_argument('--headless')   # 无界面化.
        #chrome_opt.add_argument('--disable-gpu')    # 配合上面的无界面化.
        #chrome_opt.add_argument('--window-size=400,1080')   # 设置窗口大小, 窗口大小会有影响.
        self.chrome = webdriver.Chrome(chrome_options=chrome_opt)     # 创建Chrome对象
    def LoadWeb(self,url,args=None,callback=None):
        try:
            self.chrome.get(url)     # get .
            self.chrome.implicitly_wait(10)
            if None != callback:
                callback(url,args,self.chrome.page_source)
            self.html = self.chrome.page_source
            self.url = url
            self.args=args
        except BaseException as e:
            print("$s"%e)
            self.url = None
            #self.chrome.quit();
        finally:
            #self.chrome.close();
            return self
        pass

    def Quit(self):
        self.chrome.quit()

 