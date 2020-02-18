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
            序号 =CONVERT.StrToInt (row[0])
            交易标的 =row[1]
            买方 = row[2]
            卖方 = row[3]
            交易金额 = CONVERT.UnitStrToFloat(row[4])
            币种 =row[5]
            股权转让比例 = CONVERT.StrToFloat(row[6])
            标的类型 =  row[7]
            并购方式=  row[8]
            最新进展=  row[9]
            披露日期=  row[10]
            披露日期Tag=  CONVERT.DateToInt(row[10])  
            最新公告日=  row[11]
            最新公告日Tag=  CONVERT.DateToInt(row[11])   
            item={
                       "Code":code
                      ,"Name":name
                      ,"序号":序号 
                      ,"交易标的":交易标的
                      ,"买方":买方
                      ,"卖方":卖方
                      ,"交易金额":交易金额
                      ,"币种":币种
                      ,"股权转让比例":股权转让比例
                      ,"标的类型":标的类型
                      ,"并购方式":并购方式
                      ,"最新进展":最新进展
                      ,"披露日期":披露日期
                      ,"披露日期Tag":披露日期Tag
                      ,"最新公告日":最新公告日
                      ,"最新公告日Tag":最新公告日Tag
                  } 
            dictName="PreData:股票:%s:并购重组"%code
            r.SortDictSave(dictName,json.dumps(item,ensure_ascii=False),最新公告日Tag)
            print(item)
    pass
r.TraverseQueue("PreProcTask:并购重组",callback)
print("OK")