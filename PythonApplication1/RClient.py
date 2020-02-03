import redis
import json
import py02
import sys
 
class RClient:
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    password = None

    @staticmethod
    def GetInst():
        inst = RClient()
        return inst
        pass

    def __init__(self):
        super().__init__()
        pass

    def __KeyBuilder(self,prefix1,prefix2,key):
        key = "%s:%s:%s" % (prefix1,prefix2,key)
        return key
        pass
    def __KeyBuilder2(self,prefix1,prefix2,prefix3,key):
        key = "%s:%s:%s:%s" % (prefix1,prefix2,prefix3,key)
        return key
        pass
    def __GetDB(self,dbIndex=0): 
        r = redis.Redis(connection_pool=self.pool ,db=dbIndex)
        return r
        pass 

    def SortDictSave(self,dictName,jsonVal,sort): 
        r = redis.Redis(connection_pool=self.pool ,db=0)
        jsonStr = ""
        if type(jsonVal) == type({}):
            jsonStr = json.dumps(jsonVal , ensure_ascii=False)
        elif type(jsonVal) == type(""):
            jsonStr = jsonVal 
        r.zadd(dictName, {jsonStr:sort})
        pass    
    def SortDictGetMax(self,dictName): 
        r = redis.Redis(connection_pool=self.pool ,db=0)
        val = r.zrevrangebyscore(dictName,sys.maxsize,-1)
        return val
        pass
    def SetSave(self,dictName,jsonVal): 
        r = redis.Redis(connection_pool=self.pool ,db=0)
        jsonStr = ""
        if type(jsonVal) == type({}):
            jsonStr = json.dumps(jsonVal , ensure_ascii=False)
        elif type(jsonVal) == type(""):
            jsonStr = jsonVal 
        r.sadd(dictName, jsonStr)
        pass    
    def DictSave(self,dictName,key,jsonVal): 
        r = redis.Redis(connection_pool=self.pool ,db=0)
        jsonStr = ""
        if type(jsonVal) == type({}):
            jsonStr = json.dumps(jsonVal , ensure_ascii=False)
        elif type(jsonVal) == type(""):
            jsonStr = jsonVal 
        r.hset(dictName,key, jsonStr)
        pass    
    def DictKeys(self,dictName): 
        r = redis.Redis(connection_pool=self.pool ,db=0) 
        _keys = r.hkeys(dictName)
        return _keys
        pass    
    def SortDictSaveArray(self,dictName,dataDict):
        r = redis.Redis(connection_pool=self.pool ,db=0)
        jsonStr = json.dumps(jsonVal ,ensure_ascii=False) 
        r.zadd(dictName, dataDict)
        pass    

    def QueryKeys(self,pattern):
        r = self.__GetDB(0)
        keys = r.scan(0,pattern,1000000)
        return keys
        pass
    def DeleteKeys(self,pattern):
        r = self.__GetDB(0)
        keys = r.scan(0,pattern,1000000)
        for key in keys[1]:
            r.delete(key)
            print("Delete %s" % key)
        return keys
        pass
    def QueueEn(self,qName,jsonVal):
        r = self.__GetDB(0)
        jsonStr = ""
        if type(jsonVal) == type({}):
            jsonStr = json.dumps(jsonVal , ensure_ascii=False)
        elif type(jsonVal) == type(""):
            jsonStr = jsonVal
        if(0 < len(jsonStr)):            
            r.rpush(qName,jsonStr)
        pass

    def QueueDe(self,qName):
        r = self.__GetDB(0)          
        val = r.lpop(qName)
        return val
        pass    
    def Count(self,qName):
        r = self.__GetDB(0)          
        val = r.llen(qName)
        return val
        pass    
    def TraverseQueue(self,qName,callback):
        r = self.__GetDB(0)
        length = r.llen(qName)
        index = 0
        while index < length:
            item = r.lindex(qName,index=index)
            callback(qName,item)
            index+=1
            #length = r.llen(qName)
        pass
    def TraverseSortedSet(self,qName,callback):
        r = self.__GetDB(0)
        arr = r.zrevrangebyscore(qName,max=sys.maxsize,min=  0,withscores=True)
        for item in arr:
            callback(qName,item)
        pass
    def ProcQueue(self,qName,callback):
        r = self.__GetDB(0)
        length = r.llen(qName)
        while 0 < length:
            item = r.lpop(qName)
            callback(qName,item)
            length = r.llen(qName)
        pass
      