from RClient import RClient
import json
from CONVERTOR import CONVERT
from CHECKER import CHECKER
import urllib.parse

r=RClient.GetInst()

def callback(qName,input):
    #print(input)
    data=json.loads(input)
    code = data["Code"].strip()
    name = data["Name"].strip()
    dateTag = CONVERT.StrToInt(data["DateTag"])
    article = data["Article"]
    uri =urllib.parse.urlparse(data["Uri"].strip())
    hostname=uri.hostname
    scheme=uri.scheme
    #print(article)
    points = article.split("\n")
    for point in points:
        point = point.strip()
        if(5<=len(point) and CHECKER.HasHanZi(point)):
            print(point)
            item={"Code":code,"Name":name,"Section":point, "DateTag":dateTag}
            dictName="PreData:股票:%s:核心题材"%code
            r.SortDictSave(dictName,item,dateTag)
    pass
r.TraverseQueue("PreProcTask:核心题材",callback)
print("OK")