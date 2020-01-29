from RClient import RClient
import json
from CONVERTOR import CONVERT
from CHECKER import CHECKER

r=RClient.GetInst()

def callback(qName,input):
    print(input)
    data=json.loads(input)
    code = data["Code"].strip()
    name = data["Name"].strip()
    table=data["Tables"][2]
    rows=table["body"]
    for row in rows:
        日期 = CONVERT.DateToInt(row[0])
        收盘价 =CONVERT.StrToFloat(row[1])
        涨跌幅 = CONVERT.StrToFloat(row[2].replace("%",""))

        主力净流入净额 = row[3]
        if True == CHECKER.EndWith(主力净流入净额,"万"):
           主力净流入净额 = 主力净流入净额.replace("万","")
           主力净流入净额= CONVERT.StrToFloat(主力净流入净额)
        elif True == CHECKER.EndWith(主力净流入净额,"亿"):
            主力净流入净额 = 主力净流入净额.replace("亿","")
            主力净流入净额 = CONVERT.StrToFloat(主力净流入净额)*10000

        主力净流入净占比 =  CONVERT.StrToFloat(row[4].replace("%",""))
        
        超大单净流入净额 = row[5]        
        if True == CHECKER.EndWith(超大单净流入净额,"万"):
            超大单净流入净额= 超大单净流入净额.replace("万","")
            超大单净流入净额 = CONVERT.StrToFloat(超大单净流入净额)
        elif True == CHECKER.EndWith(超大单净流入净额,"亿"):
            超大单净流入净额 = 超大单净流入净额.replace("亿","")
            超大单净流入净额 = CONVERT.StrToFloat(超大单净流入净额)*10000


        超大单净流入净占比 =  CONVERT.StrToFloat(row[6].replace("%",""))
       
        大单净流入净额 = row[7]
        if True == CHECKER.EndWith(大单净流入净额,"万"):
            大单净流入净额= 大单净流入净额.replace("万","")
            大单净流入净额 = CONVERT.StrToFloat(大单净流入净额)
        elif True == CHECKER.EndWith(大单净流入净额,"亿"):
            大单净流入净额 =大单净流入净额.replace("亿","")
            大单净流入净额 = CONVERT.StrToFloat(大单净流入净额)*10000
 

        大单净流入净占比 = CONVERT.StrToFloat(row[8].replace("%",""))
        
        中单净流入净额 = row[9]
        if True == CHECKER.EndWith(中单净流入净额,"万"):
            中单净流入净额 = 中单净流入净额.replace("万","")
            中单净流入净额 = CONVERT.StrToFloat(中单净流入净额)
        elif True == CHECKER.EndWith(中单净流入净额,"亿"):
            中单净流入净额 = 中单净流入净额.replace("亿","")
            中单净流入净额 = CONVERT.StrToFloat(中单净流入净额)*10000

        中单净流入净占比	 = CONVERT.StrToFloat(row[10].replace("%",""))

        小单净流入净额 = row[11]
        if True == CHECKER.EndWith(小单净流入净额,"万"):
            小单净流入净额 = 小单净流入净额.replace("万","")
            小单净流入净额 = CONVERT.StrToFloat(小单净流入净额)
        elif True == CHECKER.EndWith(小单净流入净额,"亿"):
            小单净流入净额 = 小单净流入净额.replace("亿","")
            小单净流入净额 = CONVERT.StrToFloat(小单净流入净额)*10000

        小单净流入净占比 =  CONVERT.StrToFloat(row[12].replace("%",""))
        item={
                   "Code":code
                  ,"Name":name
                  ,"日期":日期
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
        dictName="股票:历史资金流向一览:%s"%code
        r.SortDictSave(dictName,json.dumps(item,ensure_ascii=False),日期)
    pass
r.ProcQueue("PreProcTask:资金流向全览",callback)
print("OK")