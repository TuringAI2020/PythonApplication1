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
        if  15== len(row):
            序号 = CONVERT.StrToInt(row[0])
            交易日期 = row[1]
            交易日期Tag = CONVERT.DateToInt(row[1]) 
            涨跌幅 = CONVERT.StrToFloat( row[2])
            收盘价 =CONVERT.StrToFloat( row[3])
            成交价 = CONVERT.StrToFloat(row[4])
            折溢率 =  CONVERT.StrToFloat( row[5])
            成交量=  CONVERT.StrToFloat(row[6]) 
            成交额 = CONVERT.StrToFloat(row[7]) 
            成交额流通市值比例 = CONVERT.PercentStrToFloat( row[8] )
            买方营业部 = row[9] 
            卖方营业部 = row[10] 
            上榜后涨跌幅1日 = CONVERT.StrToFloat(row[11])
            上榜后涨跌幅5日 = CONVERT.StrToFloat(row[12] )
            上榜后涨跌幅10日 =CONVERT.StrToFloat( row[13])
            上榜后涨跌幅20日 =CONVERT.StrToFloat( row[14] )
            item={
                       "Code":code
                      ,"Name":name
                      ,"序号":序号
                      ,"交易日期":交易日期
                      ,"交易日期Tag":交易日期Tag
                      ,"涨跌幅":涨跌幅
                      ,"收盘价":收盘价
                      ,"成交价":成交价
                      ,"折溢率":折溢率
                      ,"成交量":成交量
                      ,"成交额":成交额
                      ,"成交额流通市值比例":成交额流通市值比例
                      ,"买方营业部":买方营业部
                      ,"卖方营业部":卖方营业部
                      ,"上榜后涨跌幅1日":上榜后涨跌幅1日
                      ,"上榜后涨跌幅5日":上榜后涨跌幅5日
                      ,"上榜后涨跌幅10日":上榜后涨跌幅10日 
                      ,"上榜后涨跌幅20日":上榜后涨跌幅20日 
                  } 
            dictName="PreData:股票:%s:大宗交易"%code
            r.SortDictSave(dictName,json.dumps(item,ensure_ascii=False),交易日期Tag)
            print(item)
    pass
r.TraverseQueue("PreProcTask:大宗交易",callback)
print("OK")