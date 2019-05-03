
#from datetime import datetime 
#print(datetime.now());

#def show(x):
#    return "wangjun";

#print(show(''))


#import urllib3

#url="http://www.runoob.com/w3cnote/python-pip-install-usage.html"
#http = urllib3.PoolManager()
#up=http.request('GET', url)#打开目标页面，存入变量up

#print(up.data)
import sys
import gzip
import urllib
import urllib.request
import io  #StringIO模块就是在内存中读写str
#import urllib2
#import urllib3
# 1. 导入Python SSL处理模块
import ssl
 
# 2. 表示忽略未经核实的SSL证书认证
context = ssl._create_unverified_context()
 
url = "https://www.toutiao.com/a6686715613953393159/"#此处为没有经过CA认证的URL地址。
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
request = urllib.request.Request(url, headers = headers)
# 3. 在urlopen()方法里 指明添加 context 参数
response = urllib.request.urlopen(request, context = context)
html = str( response.read(), encoding = "utf8") 
buf = io.StringIO(html) #将读取的response信息作为stringIO方便后面作为文件写入
f = gzip.GzipFile(fileobj=buf)  #解压缩response
data = f.read() 
print(data)
 
print(s)