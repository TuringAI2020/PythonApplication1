from CHECKER import CHECKER

class CONVERT:
    @staticmethod
    def DateToInt(input):
        input=input.replace('-','').replace('/','')
        val =  int(input)
        return val
        pass
    @staticmethod
    def CodeToInt(input):
        input="1"+input
        val =  int(input)
        return val
        pass
    @staticmethod
    def StrToFloat(input):
        if True == CHECKER.IsNumber(input):
            val =  float(input)
            return val
        else: 
            return 0.0
        pass
    @staticmethod
    def StrToInt(input):
        val =  int(input)
        return val
        pass

    @staticmethod
    def PercentStrToFloat(input):
        input = input.replace("%","")
        val =  float(input)
        return val
        pass

    @staticmethod
    def UnitStrToFloat(input):
        if True == CHECKER.EndWith(input,"万"):
            input= input.replace("万","")
            input = CONVERT.StrToFloat(input)
        elif True == CHECKER.EndWith(input,"亿"):
            input = input.replace("亿","")
            input = CONVERT.StrToFloat(input)*10000
        else:
            input = CONVERT.StrToFloat(input)/10000.0
        return input
        pass