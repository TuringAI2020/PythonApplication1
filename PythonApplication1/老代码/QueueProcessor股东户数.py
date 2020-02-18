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
        if  13== len(row):
            股东户数统计截止日 = row[0]
            股东户数统计截止日Tag = CONVERT.DateToInt(股东户数统计截止日)
            区间涨跌幅 =  CONVERT.StrToFloat(row[1])
            股东户数本次 = CONVERT.StrToFloat( row[2])
            股东户数上次 = CONVERT.StrToFloat( row[3]) 
            股东户数增减 =  CONVERT.StrToFloat( row[4])
            股东户数增减比例=  CONVERT.StrToFloat(row[5]) 
            户均持股市值 = CONVERT.StrToFloat(row[6]) 
            户均持股数量 = CONVERT.StrToFloat(row[7] )
            总市值 = CONVERT.StrToFloat(row[8] )
            总股本 = CONVERT.StrToFloat(row[9] )
            股本变动 = CONVERT.UnitStrToFloat(row[10] )
            股本变动原因 = row[11] 
            股东户数公告日期 = row[12]
            股东户数公告日期Tag = CONVERT.DateToInt(股东户数公告日期)
            item={
                       "Code":code
                      ,"Name":name
                      ,"股东户数统计截止日":股东户数统计截止日
                      ,"股东户数统计截止日Tag":股东户数统计截止日Tag
                      ,"区间涨跌幅":区间涨跌幅
                      ,"股东户数本次":股东户数本次
                      ,"股东户数上次":股东户数上次
                      ,"股东户数增减":股东户数增减
                      ,"股东户数增减比例":股东户数增减比例
                      ,"户均持股市值":户均持股市值
                      ,"户均持股数量":户均持股数量
                      ,"总市值":总市值
                      ,"总股本":总股本
                      ,"股本变动":股本变动
                      ,"股本变动原因":股本变动原因
                      ,"股东户数公告日期":股东户数公告日期
                      ,"股东户数公告日期Tag ":股东户数公告日期Tag 
 
                  } 
            dictName="PreData:股票:%s:股东户数"%code
            r.SortDictSave(dictName,json.dumps(item,ensure_ascii=False),股东户数统计截止日Tag)
            print(item)
    pass
r.DeleteKeys("PreData:股票:*:股东户数")
r.TraverseQueue("PreProcTask:股东户数",callback)
print("OK")