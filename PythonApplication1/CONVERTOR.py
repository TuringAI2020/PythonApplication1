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
        val =  float(input)
        return val
        pass

    