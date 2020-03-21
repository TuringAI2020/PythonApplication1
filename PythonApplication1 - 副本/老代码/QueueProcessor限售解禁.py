from RClient import RClient
import json
from CONVERTOR import CONVERT
from CHECKER import CHECKER
import sys

r=RClient.GetInst()

def callback(qName,input):
    这个有问题
    #input = input.encode(encoding= "gbk").decode(encoding="utf-8") 
    #print(input)
    test=u'\u7528\u4f8b\u540d\u79f0'.encode().decode('unicode-escape')
    data=json.loads(input)
    code = data["Code"].strip()
    name = data["Name"].strip()
    tables = data["Tables"]
    if 4!=len(tables):
        return None

    table=data["Tables"][2]
    rows=table["body"]
    for row in rows:
        if  14== len(row):
            序号 =CONVERT.StrToInt (row[0])
            解禁时间 = row[1]
            解禁时间Tag = CONVERT.DateToInt(row[1]) 
            解禁股东数 = CONVERT.StrToInt(row[2].encode('utf-8').decode('gbk'))
            解禁数量 =CONVERT.UnitStrToFloat(row[4].encode('utf-8').decode('gbk'))
            实际解禁数量 = CONVERT.UnitStrToFloat(row[5].encode('utf-8').decode('gbk'))
            未解禁数量 =  CONVERT.UnitStrToFloat( row[6].encode('utf-8').decode('gbk'))
            实际解禁市值=  CONVERT.UnitStrToFloat(row[7].encode('utf-8').decode('gbk'))  
            占总市值比例=  CONVERT.StrToFloat(row[8])  
            占流通市值比例=  CONVERT.StrToFloat(row[9])  
            解禁前一日收盘价=  CONVERT.StrToFloat(row[10])  
            限售股类型=  row[11]
            解禁前20日涨跌幅=  CONVERT.StrToFloat(row[12])  
            解禁后20日涨跌幅=  CONVERT.StrToFloat(row[13])  
            item={
                       "Code":code
                      ,"Name":name
                      ,"序号":序号
                      ,"解禁时间":解禁时间
                      ,"解禁时间Tag":解禁时间Tag
                      ,"解禁股东数":解禁股东数
                      ,"解禁数量":解禁数量
                      ,"实际解禁数量":实际解禁数量
                      ,"未解禁数量":未解禁数量
                      ,"实际解禁市值":实际解禁市值
                      ,"占总市值比例":占总市值比例
                      ,"占流通市值比例":占流通市值比例
                      ,"解禁前一日收盘价":解禁前一日收盘价
                      ,"限售股类型":限售股类型
                      ,"解禁前20日涨跌幅":解禁前20日涨跌幅
                      ,"解禁后20日涨跌幅":解禁后20日涨跌幅
                  } 
            dictName="PreData:股票:%s:限售解禁"%code
            #r.SortDictSave(dictName,json.dumps(item,ensure_ascii=False),日期Tag)
            print(item)
    pass
r.TraverseQueue("PreProcTask:限售解禁",callback)
print("OK")