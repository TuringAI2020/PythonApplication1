from RClient import RClient
import json
from CONVERTOR import CONVERT
from CHECKER import CHECKER

r=RClient.GetInst()

def callback(qName,input):
    #print(input)
    data=json.loads(input)
    code = data["Code"].strip()
    name = data["Name"].strip()
    tables = data["Tables"]
    if 3!=len(tables):
        return None

    table=data["Tables"][2]
    rows=table["body"]
    for row in rows:
        if  8== len(row):
            序号 =CONVERT.StrToInt (row[0])
            机构名称 = row[1]
            日期Tag = CONVERT.GetCurrentDateTag() 
            机构属性 = row[3]
            持股总数 =CONVERT.StrToFloat(row[4])
            持股市值 = CONVERT.StrToFloat(row[5])
            占总股本比例 =  CONVERT.StrToFloat( row[6])
            占流通股本比例=  CONVERT.StrToFloat(row[7])  
            item={
                       "Code":code
                      ,"Name":name
                      ,"序号":序号
                      ,"日期Tag":日期Tag
                      ,"机构属性":机构属性
                      ,"持股总数":持股总数
                      ,"持股市值":持股市值
                      ,"占总股本比例":占总股本比例
                      ,"占流通股本比例":占流通股本比例
                  } 
            dictName="PreData:股票:%s:主力持仓"%code
            r.SortDictSave(dictName,json.dumps(item,ensure_ascii=False),日期Tag)
            print(item)
    pass
r.TraverseQueue("PreProcTask:主力持仓",callback)
print("OK")