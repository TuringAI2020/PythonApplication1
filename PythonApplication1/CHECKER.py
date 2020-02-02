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
        reg1 = re.compile("^\d+.*\d*$")  #检查中文)
        res1 =  reg1.search(input.strip())
        if None!=res1:
            return True
        
        reg2= re.compile("^-*(\d{1,3},*)+.*\d+$")  #检查中文)
        res2 =  reg2.search(input.strip())
        if None!=res2:
            return True

        return False
        pass
    @staticmethod
    def IsDate(input):
        reg1 = re.compile("^[0-9][0-9][-/][0-1][0-9][-/][0-3][0-9]$")  #检查中文) 19-09-19
        res1 =  reg1.search(input.strip())
        if None!=res1:
            return True

        reg2 = re.compile("^[2][0][0-9][0-9][-/][0-1][0-9][-/][0-3][0-9]$")  #检查中文) 19-09-19
        res2 =  reg2.search(input.strip())
        if None!=res2:
            return True

        return False
        pass

    pass
  