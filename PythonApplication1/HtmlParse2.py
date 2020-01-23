import sys
import os
import re
from bs4 import BeautifulSoup
import redis
import json
 
for root, dirs,files in os.walk("D:\Desktop"):
    for file in files:
    #soup1 = BeautifulSoup(open("D:\Desktop\上工申贝(600843)资金流向全览 _ 数据中心 _ 东方财富网-2020-01-08.txt","r",encoding="utf-8")) 
    #soup1  = soup1.prettify()
        data={"Code":"","Name":"","hxtc":[]}
        path="%s\\%s"%(root,file)

        name=file.split('(')[0]
        code = file.split('(')[1].split(')')
        dateTag=int(file.split("— 东方财富网-")[1].split(".txt")[0].replace("-",""))
        if(re.match("^.*资金流向全览.*\.txt$",file)):
            print(file)

            data["Name"]=name
            data["Code"]=code
            soup1 = BeautifulSoup(open(path,"r",encoding="utf-8")) 
            trArr = soup1.find(id="dt_1").find("tbody").find_all("tr")
            for tr in trArr:
                tdArr = tr.find_all("td")
                if(13==len(tdArr)):
                    date=tdArr[0].text 
                    spj=float(tdArr[1].text )
                    zdf=float(tdArr[2].text.replace("%","") )
                    zljlr_je=float(tdArr[3].text.replace("万","") )
                    zljlr_jzb=float(tdArr[4].text.replace("%","") )
                    cddjlr_je=float(tdArr[5].text.replace("万","") )
                    cddjlr_jzb=float(tdArr[6].text.replace("%","") )
                    ddjlr_je=float(tdArr[7].text.replace("万","") )
                    ddjlr_jzb=float(tdArr[8].text.replace("%","") )
                    zdjlr_je=float(tdArr[9].text.replace("万","") )
                    zdjlr_jzb=float(tdArr[10].text.replace("%","") )
                    xdjlr_je=float(tdArr[11].text.replace("万","") )
                    xdjlr_jzb=float(tdArr[12].text.replace("%","") )
                    item={"date":date,"spj":spj,"zdf":zdf,"zljlr_je":zljlr_je,"zljlr_jzb":zljlr_jzb,"cddjlr_je":cddjlr_je,"ddjlr_je":ddjlr_je,"zdjlr_je":zdjlr_je,"zdjlr_jzb":zdjlr_jzb,"xdjlr_je":xdjlr_je}
                    #print(item)
        elif  (re.match("^.*股票_数据_资料_信息.*\.txt$",file)):
            print(file)
            soup2 = BeautifulSoup(open(path,"r",encoding="utf-8")) 
            hxtcArr = soup2.select('#m_hxtc .content p')#核心题材
            hxtcList=[]
            for hxtc in hxtcArr:
                title=hxtc.select("b")[0].text
                val= hxtc.text
                item={"Code":code,"Name":Name,"DateTag":"","Title":title,"Value":val}
                print(item)
                m_cwzy_valArr = soup2.select_one("#m_cwzy tbody tr")#财务摘要
                for m_cwzy in m_cwzy_valArr:
                    #print(m_cwzy)
                    pass
            重点关注类型={}
            m_zdgz_TitleArr = soup2.select("#zdgzContent .itemtitle")
            for m_zdgz_title in m_zdgz_TitleArr:
                print(m_zdgz_title.text)
                if(m_zdgz_title.text in 重点关注类型):
                    重点关注类型[m_zdgz_title.text]+=1
                else:
                    重点关注类型[m_zdgz_title.text]=1
            重点关注标题={}
            m_zdgz_ItemArr = soup2.select("#zdgzContent .item")
            for m_zdgz_item in m_zdgz_ItemArr:
                #print(m_zdgz_item.text)
                if(m_zdgz_item.text in 重点关注标题):
                    重点关注标题[m_zdgz_item.text]+=1
                else:
                    重点关注标题[m_zdgz_item.text]=1
            #print(重点关注标题)
print('全部结束')
#股票:核心题材:编码:日期