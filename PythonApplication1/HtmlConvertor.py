from bs4 import BeautifulSoup
import re
import json
import CHECKER

class HtmlConvertor:
    __pageSource="<html></html>"
    __pageData={"Uri":"","Title":"","Links":[],"Tables":[],"Article":""}
    __uri=""
    __soup=None
    @staticmethod
    def GetInst():
        return HtmlConvertor()
        pass
    def __FindLinks(self,links):
        arr=[]
        for link in links:
            text = link.text
            href = link["href"]
            if 0<len(text) and 0<len(href) :
                item={"Text":text,"Href":href}
                if 7<=len(href) and re.match("http://",href) :
                    item["absolute"]=1
                elif 7<=len(href) and re.match("https://",href) :
                    item["absolute"]=2
                else  :
                    item["absolute"]=0
                arr.append(item)
                pass
            pass   
        return arr 
        pass
    def __FindTables(self,tables):
        arr=[]
        tableCount= len(tables)
        tableIndex=0
        for table in tables:
            tableIndex+=1
            data={"index":tableIndex,"capital":"","id":"","head":[],"body":[]}
            thArr=table.select("thead tr")
            trArr=table.select("tbody tr")
            id=table.get("id")
            if(None != id):
                data["id"]=id
            if(0==len(trArr) and 0 == len(thArr)):
                trArr=table.select("tr")
                pass
            for tr in trArr:
                tdArr = tr.select("td,th")
                cellArr=[]
                for td in tdArr:
                    text="".join(td.text.split())
                    cellArr.append(text)
                    pass
                data["body"].append(cellArr)
                pass
            arr.append(data)            
            pass
        return arr   
        pass
    def __FindArticle(self,selector="p"):
        pArr=self.__soup.select("p")
        parentRef={}
        index=0
        for p in pArr:
            pItems = p.parent.select("%s>p"%p.parent.name)
            pCount=len(pItems)
            parentRef[index]=pCount
            index+=1
            pass
        maxVal=0
        selectIndex=-1
        for k in parentRef:
            if(maxVal<parentRef[k]):
                maxVal=parentRef[k]
                selectIndex=k

        article=""
        if -1!=selectIndex:
            container=pArr[selectIndex].parent
            article=container.text 
        return article   
        pass
    def __FindSection(self,selector):

        pass      
    def LoadFromWeb(self,url):
        pass
    def LoadFromString(self,html):
        if(type(html) == type("")):
            self.__pageSource=html
        return self            
        pass
    def LoadFromFile(self,filePath,encoding="utf-8"):
        file=open(file=filePath,mode="r",encoding=encoding)
        self.__pageSource=file.read()
        self.__uri=filePath
        return self
        pass
    def ConvertToJson(self):
        self.__soup = BeautifulSoup(self.__pageSource,features="html5lib")
        if None != self.__soup.title:
            title=self.__soup.title.text
            tables=self.__soup.select("table")
            links=self.__soup.select("a[href]")
            links = self.__FindLinks(links)
            tables = self.__FindTables(tables)
            article=self.__FindArticle(selector="p")
            self.__pageData["Uri"]=self.__uri
            self.__pageData["Title"]=title
            self.__pageData["Links"]=links
            self.__pageData["Tables"]=tables
            self.__pageData["Article"]=article
            jsonStr = json.dumps(self.__pageData, ensure_ascii=False) 
            return jsonStr 
        else:
            return None
    pass
     
#res = HtmlConvertor.GetInst().LoadFromFile(r"D:\007\t7.txt").ConvertToJson()
#print(res)