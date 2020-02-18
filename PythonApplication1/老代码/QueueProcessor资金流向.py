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
    if 3!=len(tables):
        return None

    table=data["Tables"][2]
    rows=table["body"]
    for row in rows:
        if  13== len(row):
            日期 =row[0]
            日期Tag =CONVERT.DateToInt (row[0])
            收盘价 = CONVERT.StrToFloat(row[1])
            涨跌幅 = CONVERT.PercentStrToFloat(row[2]) 
            主力净流入净额 = CONVERT.UnitStrToFloat(row[3])
            主力净流入净占比 =CONVERT.PercentStrToFloat(row[4])
            超大单净流入净额 = CONVERT.UnitStrToFloat(row[5])
            超大单净流入净占比 =  CONVERT.PercentStrToFloat( row[6])
            大单净流入净额=  CONVERT.UnitStrToFloat(row[7])  
            大单净流入净占比=  CONVERT.PercentStrToFloat(row[8])  
            中单净流入净额=  CONVERT.UnitStrToFloat(row[9])  
            中单净流入净占比=  CONVERT.PercentStrToFloat(row[10])  
            小单净流入净额=  CONVERT.UnitStrToFloat(row[11])
            小单净流入净占比=  CONVERT.PercentStrToFloat(row[12])   
            item={
                       "Code":code
                      ,"Name":name
                      ,"日期":日期
                      ,"日期Tag":日期Tag
                      ,"收盘价":收盘价
                      ,"涨跌幅":涨跌幅
                      ,"主力净流入净额":主力净流入净额
                      ,"主力净流入净占比":主力净流入净占比
                      ,"超大单净流入净额":超大单净流入净额
                      ,"超大单净流入净占比":超大单净流入净占比
                      ,"大单净流入净额":大单净流入净额
                      ,"大单净流入净占比":大单净流入净占比
                      ,"中单净流入净额":中单净流入净额
                      ,"中单净流入净占比":中单净流入净占比
                      ,"小单净流入净额":小单净流入净额
                      ,"小单净流入净占比":小单净流入净占比
                  } 
            dictName="PreData:股票:%s:资金流向"%code
            r.SortDictSave(dictName,json.dumps(item,ensure_ascii=False),日期Tag)
            print(item)
    pass
r.TraverseQueue("PreProcTask:资金流向",callback)
print("OK")