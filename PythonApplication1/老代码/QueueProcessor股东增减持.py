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
    if 1!=len(tables):
        return None

    table=data["Tables"][0]
    rows=table["body"]
    for row in rows:
        if  17== len(row):
            最新价 = CONVERT.StrToFloat(row[3]) 
            跌涨幅 =  CONVERT.PercentStrToFloat(row[4])
            股东名称 = row[5]
            持股变动信息增减 = row[6]
            持股变动信息变动数量 =  CONVERT.StrToFloat( row[7])
            持股变动信息占总股本比例=  CONVERT.PercentStrToFloat(row[8]) 
            持股变动信息占流通股比例 = CONVERT.PercentStrToFloat(row[9]) 
            变动后持股情况持股总数 = CONVERT.StrToFloat(row[10] )
            变动后持股情况占总股本比例 = CONVERT.PercentStrToFloat(row[11] )
            变动后持股情况持流通股数 = CONVERT.StrToFloat(row[12] )
            变动后持股情况占流通股比例 = CONVERT.PercentStrToFloat(row[13] )
            变动开始日 = row[14] 
            变动截止日 = row[15]
            公告日 = row[16]
            公告日Tag=0
            item={
                       "Code":code
                      ,"Name":name
                      ,"最新价":最新价
                      ,"跌涨幅":跌涨幅
                      ,"股东名称":股东名称
                      ,"持股变动信息增减":持股变动信息增减
                      ,"持股变动信息变动数量":持股变动信息变动数量
                      ,"持股变动信息占总股本比例":持股变动信息占总股本比例
                      ,"持股变动信息占流通股比例":持股变动信息占流通股比例
                      ,"变动后持股情况持股总数":变动后持股情况持股总数
                      ,"变动后持股情况占总股本比例":变动后持股情况占总股本比例
                      ,"变动后持股情况持流通股数":变动后持股情况持流通股数
                      ,"变动后持股情况占流通股比例":变动后持股情况占流通股比例
                      ,"变动开始日":变动开始日
                      ,"变动截止日":变动截止日
                      ,"公告日":公告日
                      ,"公告日Tag":公告日Tag
                  } 
            dictName="PreData:股票:%s:股东增减持"%code
            r.SortDictSave(dictName,json.dumps(item,ensure_ascii=False),公告日Tag)
            print(item)
    pass
r.TraverseQueue("PreProcTask:股东增减持",callback)
print("OK")