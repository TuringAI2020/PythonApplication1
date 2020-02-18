import re
class CHECKER:
    @staticmethod
    def HasHanZi(input):
        reg = re.compile(u'[\u4e00-\u9fa5]')  #检查中文)
        res =  reg.search(input)
        return None!=res
        pass
    pass