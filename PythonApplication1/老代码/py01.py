import redis
import json
import py02

dateStr="2020-01-21"
codeStr="001"
dateTag = py02.CONVERT.DateToInt(dateStr)
codeTag = py02.CONVERT.CodeToInt(codeStr)
jsonVal={"Name":"名称3","Code":"003","PC":[{"Date":"2020-01-20"}]}   
testdata1={"Name":"名称3","Code":"003","T":[{"DateTag":20200120,"Text":"ZREMRANGEBYLEX ZREMRANGEBYRANK ZREMRANGEBYSCORE"},{"DateTag":20200120,"Text":"Set any number of element-name, score pairs"},{"DateTag":20200121,"Text":"single element/score pair can be specified and the score is the amount"}]}
testdata2={"Name":"名称3","Code":"003","P":[{"DateTag":20200120,"P1":100,"P2":200,"P3":300,"P4":400,"P5":500,"P6":600},{"DateTag":20200121,"P1":101,"P2":201,"P3":301,"P4":401,"P5":501,"P6":601}]}

class RClient:
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    def __init__(self):
        super().__init__()
        pass

    def __KeyBuilder(self,prefix1,prefix2,key):
        key="%s:%s:%s"%(prefix1,prefix2,key)
        return key
        pass
    def __KeyBuilder2(self,prefix1,prefix2,prefix3,key):
        key="%s:%s:%s:%s"%(prefix1,prefix2,prefix3,key)
        return key
        pass
    def __GetDB(self,dbIndex=0):
        r = redis.Redis(connection_pool=self.pool,  password="Sein2019",db=dbIndex)
        return r
        pass
    def SaveItem(self,jsonVal):
        r = redis.Redis(connection_pool=self.pool,  password="Sein2019",db=0)
        keys = r.keys("*")
        for key in keys:
            print(key)
            
        jsonStr=json.dumps(jsonVal ,ensure_ascii=False)
        r.set("GP:%s_%s"%(jsonVal["Code"],jsonVal["Name"]),jsonStr)
        r.close()
    def SortDictSave(self,dictName,jsonVal,sort):
        r = redis.Redis(connection_pool=self.pool,  password="Sein2019",db=0)
        jsonStr=json.dumps(jsonVal ,ensure_ascii=False) 
        r.zadd(dictName, {jsonVal:sort})
        pass    
    def SortDictSaveArray(self,dictName,dataDict):
        r = redis.Redis(connection_pool=self.pool,  password="Sein2019",db=0)
        jsonStr=json.dumps(jsonVal ,ensure_ascii=False) 
        r.zadd(dictName, dataDict)
        pass    
    def QueryKeys(self,pattern):
        r=self.__GetDB(0)
        keys = r.scan(0,pattern,10000)
        return keys
        pass
    def QueueEn(self,qName,jsonVal):
        r=self.__GetDB(0)
        jsonStr= ""
        if type(jsonVal) == type({}):
            jsonStr = json.dumps(jsonVal)
        elif type(jsonVal) == type(""):
            jsonStr=jsonVal
        if(0<len(jsonStr)):            
            r.rpush(qName,jsonStr)
        pass
    def QueueDe(self,qName):
        r=self.__GetDB(0)          
        val = r.lpop(qName)
        return val
        pass    
    def ProcQueue(self,qName,callback):
        r = self.__GetDB(0)
        length = r.llen(qName)
        while 0<length:
            item  = r.lpop(qName)
            callback(qName,item)
            length = r.llen(qName)
        pass
    def Test1(self,jsonVal):
        code=jsonVal["Code"]
        key = self.__KeyBuilder("S1","T",code)
        arr=jsonVal["T"]
        for item in arr:
            self.SortDictSave(key,item["Text"],item["DateTag"])
            pass
        pass
    def Test2(self,jsonVal):
        code=py02.CONVERT.CodeToInt(jsonVal["Code"])
        key = self.__KeyBuilder("S1","P",code)
        arr=jsonVal["P"]
        for item in arr:
            for k in item:
                if("DateTag"!=k):
                    key=self.__KeyBuilder2("S1","P",k,code)
                    dateTag=item["DateTag"]
                    v = item[k]
                    self.SortDictSave(key,v,dateTag)
            pass
        pass
r = RClient() 
#key = r.KeyBuilder("G","N","0998")
#r.SortDictSave("Test:test1",jsonVal=jsonVal,sort=100)
# r.Test1(testdata1)
# r.Test2(testdata2)
# count=10
# while 0<count:
#     r.QueueEn("QTest",{"Test":"1234"})
#     count-=1  
# def qProc(qName,item): 
#     print(" %s"% item )    
# r.ProcQueue("QTest",qProc)
#print(r.QueueDe("QTest"))
keys = r.QueryKeys("S1:P:P5:*")
print(keys)
print('OK')