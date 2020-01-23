from selenium import webdriver
import time 
from py03 import HtmlConvertor
driver = webdriver.Chrome()     # 创建Chrome对象.
# 操作这个对象.
driver.get('http://data.eastmoney.com/stockdata/600584.html')     # get方式访问百度.
driver.implicitly_wait(10)
#print(driver.page_source)
html = driver.page_source
driver.quit()   # 使用完, 记得关闭浏览器, 不然chromedriver.exe进程为一直在内存中. 
res = HtmlConvertor.GetInst().LoadFromString(html=html).ConvertToJson()
print(res)