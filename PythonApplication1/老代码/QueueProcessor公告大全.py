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
    uri =urllib.parse.urlparse(data["Uri"].strip())
    hostname=uri.hostname
    scheme=uri.scheme
    links = data["Links"]
    table=data["Tables"][2]
    rows=table["body"]
    for row in rows:
        title=row[0].strip()
        _type = row[1].strip()
        date = row[2].strip()
        dateTag = CONVERT.DateToInt(row[2].strip())
        item={"Code":code,"Name":name,"Title":title,"Type":_type,"Date":date,"DateTag":dateTag,"Url":""}
        if type([]) == type(links):
            for link in links:
                if link["Text"].strip() == title:
                    item["Url"]="%s://%s/%s"%(scheme,hostname,link["Href"])
                    dictName="PreData:股票:%s:公告大全"%code
                    r.SortDictSave(dictName,item,dateTag)
    pass
r.TraverseQueue("PreProcTask:公告大全",callback)
#r.DeleteKeys("股票:公告大全:*")
print("OK")