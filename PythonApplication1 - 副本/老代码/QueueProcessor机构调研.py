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
    tables = data["Tables"]
    if 0==len(tables):
        return None

    table=data["Tables"][0]
    rows=table["body"]
    for row in rows:
        if(10==len(row)):
            序号=row[0]
            代码=row[1]
            名称=row[2]
            接待机构数量=CONVERT.StrToInt(row[4])
            接待方式=row[5]
            接待人员=row[6]
            接待地点=row[7]

            接待日期=row[8]
            接待日期Tag = 0
            if(10==len(接待日期)):
                接待日期Tag=CONVERT.DateToInt(接待日期)

            公告日期=row[9]
            公告日期Tag = 0
            if 10!=len(公告日期) and 10==len(接待日期):
                公告日期=接待日期.split("-")[0]+"/"+公告日期
                公告日期Tag = CONVERT.DateToInt(公告日期)


            item={
                       "Code":code
                      ,"Name":name
                      ,"序号":序号
                      ,"代码":代码
                      ,"名称":名称
                      ,"接待机构数量":接待机构数量
                      ,"接待方式":接待方式
                      ,"接待人员":接待人员
                      ,"接待地点":接待地点
                      ,"接待日期":接待日期
                      ,"接待日期Tag":接待日期Tag
                      ,"公告日期":公告日期
                      ,"公告日期Tag":公告日期Tag
                  } 
            dictName="PreData:股票:%s:机构调研"%code
            r.SortDictSave(dictName,json.dumps(item,ensure_ascii=False),接待日期Tag)
            print(item)
    pass
r.TraverseQueue("PreProcTask:机构调研",callback)
print("OK")