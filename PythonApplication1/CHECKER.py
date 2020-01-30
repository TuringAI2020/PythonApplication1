import re
class CHECKER:
    @staticmethod
    def HasHanZi(input):
        reg = re.compile(u'[\u4e00-\u9fa5]')  #检查中文)
        res =  reg.search(input)
        return None!=res
        pass

    @staticmethod
    def Contains(input,word):
        res = re.search("%s+"%word,input.strip()) 
        return None!=res
        pass

    @staticmethod
    def EndWith(input,word):
        res = re.search("%s$"%word,input.strip()) 
        return None!=res
        pass
    @staticmethod
    def IsNumber(input):
        reg = re.compile("^\d+.*\d*$")  #检查中文)
        res =  reg.search(input.strip())
        return None!=res
        pass
    pass
  