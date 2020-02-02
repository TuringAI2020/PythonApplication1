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

def IsTableHead(row): 
      for item in row:
           if True!=CHECKER.HasHanZi(item):
               return False 
      return True

def FillItemList(table):
     rows = table["body"]
     rows=rows[1:]
     if 11 != len(rows[0]):
        return None
     table["body"]=rows
     arr = CreateEmptyItemList(table)

     for row in rows:
         key = row[0]
         rowIndex = 1
         while rowIndex < len(arr):
             if True != CHECKER.IsDate(row[rowIndex]):
                 arr[rowIndex - 1][key] = CONVERT.UnitStrToFloat(row[rowIndex])
             else:
                 if 11 == len(row[rowIndex]):
                    "20" + row[rowIndex] 
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
    if 0 == len(tables):
        return None

    itemList = FillItemList(tables[0])
    if None!=itemList:
        for item in itemList:
                item["Code"] = code
                item["Name"] = name
                if "DateTag" in item:
                    dateTag=item["DateTag"]
                    dictName = "PreData:股票:%s:股东研究" % code
                    #r.SortDictSave(dictName,json.dumps(item,ensure_ascii=False),日期Tag)
                    item["较上期变化(%)"]=item["较上期变化(%)"]*10000
                    item["股价(元)"]=item["股价(元)"]*10000
                    item["前十大股东持股合计(%)"]=item["前十大股东持股合计(%)"]*10000
                    item["前十大流通股东持股合计(%)"]=item["前十大流通股东持股合计(%)"]*10000
                    print("%s %s"%(dateTag,item))
      
    pass
r.TraverseQueue("PreProcTask:股东研究",callback)
print("OK")