import time
from CHECKER import CHECKER

class CONVERT:
    @staticmethod
    def DateToInt(input):
        input = input.replace('-','').replace('/','')
        val = int(input)
        return val
        pass
    @staticmethod
    def CodeToInt(input):
        input = "1" + input
        val = int(input)
        return val
        pass
    @staticmethod
    def StrToFloat(input):
        if True == CHECKER.IsNumber(input):
            val = float(input.replace(",",""))
            return val
        else: 
            return 0.0
        pass
    @staticmethod
    def StrToInt(input):
        val = int(input)
        return val
        pass

    @staticmethod
    def PercentStrToFloat(input):
        input = input.replace("%","")
        val = CONVERT.StrToFloat(input)
        return val
        pass

    @staticmethod
    def UnitStrToFloat(input,unit="万"):

        if True == CHECKER.EndWith(input,"%"):
            output = CONVERT.PercentStrToFloat(input)
            return output


        if True == CHECKER.EndWith(input,"万亿"):
            input = input.replace("万亿","")
            input = CONVERT.StrToFloat(input) * 10000 * 10000
        elif True == CHECKER.EndWith(input,"万"):
            input = input.replace("万","")
            input = CONVERT.StrToFloat(input)
        elif True == CHECKER.EndWith(input,"亿"):
            input = input.replace("亿","")
            input = CONVERT.StrToFloat(input) * 10000
        elif unit=="万":
            input = CONVERT.StrToFloat(input) / 10000.0
        elif None == unit:
            input = CONVERT.StrToFloat(input)
        return input
        pass

    @staticmethod
    def GetCurrentDateTag():
        timeTag = time.strftime("%Y-%m-%d", time.localtime())
        dateTag = CONVERT.DateToInt(timeTag)
        return dateTag
        pass