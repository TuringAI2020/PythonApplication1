import redis
import json
import py02

 
class RClient:
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    password=None

    @staticmethod
    def GetInst():
        inst = RClient()
        return inst
        pass

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
        r = redis.Redis(connection_pool=self.pool ,db=dbIndex)
        return r
        pass 

    def SortDictSave(self,dictName,jsonVal,sort): 
        r = redis.Redis(connection_pool=self.pool ,db=0)
        jsonStr=json.dumps(jsonVal ,ensure_ascii=False) 
        r.zadd(dictName, {jsonVal:sort})
        pass    

    def SortDictSaveArray(self,dictName,dataDict):
        r = redis.Redis(connection_pool=self.pool ,db=0)
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
            jsonStr = json.dumps(jsonVal , ensure_ascii=False)
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
    def Count(self,qName):
        r=self.__GetDB(0)          
        val = r.llen(qName)
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
#keys = r.QueryKeys("S1:P:P5:*")
#print(keys)
#print('OK')