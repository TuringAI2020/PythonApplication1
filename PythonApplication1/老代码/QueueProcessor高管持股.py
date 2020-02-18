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
    if 2!=len(tables):
        return None

    table=data["Tables"][1]
    rows=table["body"]
    for row in rows:
        if  14== len(row):
            日期 = row[0]
            日期Tag = CONVERT.DateToInt(row[0]) 
            代码 =  row[1]
            名称 = row[2]
            变动人 = row[3]
            变动股数 =  CONVERT.UnitStrToFloat( row[4])
            成交均价=  CONVERT.StrToFloat(row[5]) 
            变动金额 = CONVERT.StrToFloat(row[6]) 
            变动原因 = row[7] 
            变动比例 = CONVERT.StrToFloat(row[8] )
            变动后持股数 = CONVERT.UnitStrToFloat(row[6] )
            持股种类 = row[10]
            董监高人员姓名 = row[11] 
            职务 = row[12]
            变动人与董监高的关系 = row[13] 
            item={
                       "Code":code
                      ,"Name":name
                      ,"日期":日期
                      ,"日期Tag":日期Tag
                      ,"代码":代码
                      ,"名称":名称
                      ,"变动人":变动人
                      ,"变动股数":变动股数
                      ,"成交均价":成交均价
                      ,"变动金额":变动金额
                      ,"变动原因":变动原因
                      ,"变动比例":变动比例
                      ,"变动后持股数":变动后持股数
                      ,"持股种类":持股种类
                      ,"董监高人员姓名":董监高人员姓名
                      ,"职务":职务
                      ,"变动人与董监高的关系":变动人与董监高的关系 
                  } 
            dictName="PreData:股票:%s:高管持股"%code
            r.SortDictSave(dictName,json.dumps(item,ensure_ascii=False),日期Tag)
            print(item)
    pass
r.TraverseQueue("PreProcTask:高管持股",callback)
print("OK")