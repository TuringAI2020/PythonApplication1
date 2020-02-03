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
    if 2!=len(tables):
        return None

    table=data["Tables"][1]
    rows=table["body"]
    for row in rows:
        if  16== len(row):
            序号	 = CONVERT.StrToInt( row[0])
            日期 =row[1]
            日期Tag =CONVERT.DateToInt (row[1])
            收盘价 = CONVERT.StrToFloat(row[3])
            涨跌幅 = CONVERT.PercentStrToFloat(row[4]) 
            后1日涨跌幅 = CONVERT.PercentStrToFloat(row[5])
            后2日涨跌幅  =CONVERT.PercentStrToFloat(row[6])
            后3日涨跌幅  = CONVERT.PercentStrToFloat(row[7])
            后5日涨跌幅  =  CONVERT.PercentStrToFloat( row[8])
            后10日涨跌幅=  CONVERT.PercentStrToFloat(row[9])  
            后20日涨跌幅=  CONVERT.PercentStrToFloat(row[10])  
            后30日涨跌幅=  CONVERT.PercentStrToFloat(row[11])  
            上榜营业部买入合计=  CONVERT.StrToFloat(row[12])  
            上榜营业部卖出合计=  CONVERT.StrToFloat(row[13])
            上榜营业部买卖净额=  CONVERT.StrToFloat(row[14])   
            上榜原因= row[15]
            item={
                       "Code":code
                      ,"Name":name
                      ,"序号":序号
                      ,"日期":日期
                      ,"日期Tag":日期Tag
                      ,"收盘价":收盘价
                      ,"涨跌幅":涨跌幅
                      ,"后1日涨跌幅":后1日涨跌幅
                      ,"后2日涨跌幅":后2日涨跌幅
                      ,"后3日涨跌幅":后3日涨跌幅
                      ,"后5日涨跌幅":后5日涨跌幅
                      ,"后10日涨跌幅":后10日涨跌幅
                      ,"后20日涨跌幅":后20日涨跌幅
                      ,"后30日涨跌幅":后30日涨跌幅
                      ,"上榜营业部买入合计":上榜营业部买入合计
                      ,"上榜营业部卖出合计":上榜营业部卖出合计
                      ,"上榜营业部买卖净额":上榜营业部买卖净额
                      ,"上榜原因":上榜原因
                  } 
            dictName="PreData:股票:%s:龙虎榜单历次上榜"%code
            r.SortDictSave(dictName,json.dumps(item,ensure_ascii=False),日期Tag)
            print(item)
    pass
r.TraverseQueue("PreProcTask:龙虎榜单历次上榜",callback)
print("OK")