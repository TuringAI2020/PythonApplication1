from RClient import RClient
import json
from CONVERTOR import CONVERT
from CHECKER import CHECKER 

r=RClient.GetInst()

def callback(qName,input): 
    #input = input.encode(encoding= "gbk").decode(encoding="utf-8") 
    #print(input) 
    data=json.loads(input)
    code = data["Code"].strip()
    name = data["Name"].strip()
    tables = data["Tables"]
    #if 9!=len(tables):
    #    return None

    tables=data["Tables"]
    for table in tables: 
        rows=table["body"]
        rowIndex=0
        item={}
        head=rows[0]
        rows=rows[1:]
        for row in rows:
            if  9== len(row):
               日期Tag=CONVERT.DateToInt(head[0])
               item={
                        "Code":code
                        ,"Name":name
                        ,"日期":head[0]
                        ,"日期Tag":日期Tag
                        ,"分类":row[0]
                        ,"主营构成":row[1]
                        ,"主营收入":CONVERT.UnitStrToFloat(row[2])
                        ,"收入比例":CONVERT.PercentStrToFloat(row[3])
                        ,"主营成本":CONVERT.UnitStrToFloat(row[4])
                        ,"成本比例":CONVERT.PercentStrToFloat(row[5])
                        ,"主营利润":CONVERT.UnitStrToFloat(row[6])
                        ,"利润比例":CONVERT.PercentStrToFloat(row[7])
                        ,"毛利率":CONVERT.PercentStrToFloat(row[8])
                        }
            dictName="PreData:股票:%s:经营分析"%code
            r.SortDictSave(dictName,json.dumps(item,ensure_ascii=False),日期Tag)
            print(item)
    pass
r.TraverseQueue("PreProcTask:经营分析",callback)
print("OK")