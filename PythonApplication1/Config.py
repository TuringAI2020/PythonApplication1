

class Cfg:
    __baseProcUrl="http://122.51.159.248:5000/YunStock2Service"
    __baseTaskUrl="http://122.51.159.248:5000/YunStockTaskService"
    #__baseProcUrl="http://127.0.0.1:5000/YunStock2Service"
    @staticmethod
    def GetProcAPIUrl(keyName=None):
        url="%s?keyName=%s"%(Cfg.__baseProcUrl,keyName)
        return url
    
    @staticmethod
    def GetTaskAPIUrl(method=None):
        url="%s?method=%s"%(Cfg.__baseTaskUrl,method)
        return url
    pass
