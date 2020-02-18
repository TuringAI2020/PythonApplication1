from RClient import RClient
import json
from CONVERTOR import CONVERT
from CHECKER import CHECKER 

r = RClient.GetInst()

def CreateEmptyItem(table):
    rows = table["body"]
    item = {}
    for row in rows:
         item[row[0].strip()] = ""
    return item

def CreateEmptyItemList(table):
    rows = table["body"]
    itemCount = 0
    arr = []
    if(0 < len(rows)):
        itemCount = len(rows[0]) - 1
    while 0 < itemCount:
        item = CreateEmptyItem(table)
        arr.append(item)
        itemCount-=1
    return arr

def FillItemList(table):
     arr = CreateEmptyItemList(table)
     rows = table["body"]
     
     for row in rows:
         key = row[0]
         rowIndex = 1
         while rowIndex < len(arr):
             if True != CHECKER.IsDate(row[rowIndex]): 
                arr[rowIndex - 1][key] = CONVERT.UnitStrToFloat(row[rowIndex],unit=None)
             else:
                 if 8 == len(row[rowIndex]):
                     row[rowIndex] = "20" + row[rowIndex] 
                 arr[rowIndex - 1][key + "Tag"] = CONVERT.DateToInt(row[rowIndex])
                 arr[rowIndex - 1][key] = row[rowIndex] 
                 arr[rowIndex - 1]["DateTag"] = CONVERT.DateToInt(row[rowIndex])
                
             rowIndex+=1
     return arr
def callback(qName,input): 
    #print(input)
    data = json.loads(input)
    code = data["Code"].strip()
    name = data["Name"].strip()
    tables = data["Tables"] 

    tables = data["Tables"]
    for table in tables:  
        itemList = FillItemList(table)
        for item in itemList:
            item["Code"] = code
            item["Name"] = name
            if "DateTag" in item:
                dateTag=item["DateTag"] 
 
                dictName = "PreData:股票:%s:新财务分析" % code
                r.SortDictSave(dictName,json.dumps(item,ensure_ascii=False),dateTag)
                print("%s %s"%(dateTag,item))
    pass
r.DeleteKeys("PreData:股票:*:新财务分析")
r.TraverseQueue("PreProcTask:新财务分析",callback)
print("OK")