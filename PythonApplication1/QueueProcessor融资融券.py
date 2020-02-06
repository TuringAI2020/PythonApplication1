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
        if 15 == len(row):
            交易日期 = row[0]
            交易日期Tag = CONVERT.DateToInt(交易日期)
            收盘价 =  CONVERT.StrToFloat(row[1])
            涨跌幅 = CONVERT.StrToFloat( row[2])
            融资余额 = CONVERT.UnitStrToFloat( row[3]) 
            融资余额占流通市值比 =  CONVERT.PercentStrToFloat( row[4])
            融资买入额 =  CONVERT.UnitStrToFloat(row[5]) 
            融资偿还额 = CONVERT.UnitStrToFloat(row[6]) 
            融资净买入 = CONVERT.UnitStrToFloat(row[7] )
            融券余额 = CONVERT.UnitStrToFloat(row[8] )
            融券余量 = CONVERT.UnitStrToFloat(row[9] )
            融券卖出量 = CONVERT.UnitStrToFloat(row[10] )
            融券偿还量 =CONVERT.UnitStrToFloat( row[11] )
            融券净卖出 =CONVERT.UnitStrToFloat( row[12] )
            融资融券余额 =CONVERT.UnitStrToFloat( row[13] )
            融资融券余额差值 =CONVERT.UnitStrToFloat( row[14] )
             
            item={
                       "Code":code
                      ,"Name":name
                      ,"交易日期":交易日期
                      ,"交易日期Tag":交易日期Tag
                      ,"收盘价":收盘价
                      ,"涨跌幅":涨跌幅
                      ,"融资余额":融资余额
                      ,"融资余额占流通市值比":融资余额占流通市值比
                      ,"融资买入额":融资买入额
                      ,"融资偿还额":融资偿还额
                      ,"融资净买入":融资净买入
                      ,"融券余额":融券余额
                      ,"融券余量":融券余量
                      ,"融券卖出量":融券卖出量
                      ,"融券偿还量":融券偿还量
                      ,"融券净卖出":融券净卖出
                      ,"融资融券余额":融资融券余额
                      ,"融资融券余额差值":融资融券余额差值
                  } 
            dictName="PreData:股票:%s:融资融券"%code
            r.SortDictSave(dictName,json.dumps(item,ensure_ascii=False),交易日期Tag)
            print(item)
    pass
r.DeleteKeys("PreData:股票:*:融资融券")
r.TraverseQueue("PreProcTask:融资融券",callback)
print("OK")