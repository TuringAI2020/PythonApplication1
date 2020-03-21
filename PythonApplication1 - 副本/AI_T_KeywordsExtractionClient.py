import requests

res = requests.post("http://127.0.0.1/YunAIService",data={"method":"TextClassification","req":"被问及法国为什么不采取意大利式的封锁，法国政府发言人 NDIAYE 公开蔑视意大利政府的措施：在欧洲，他们第一个中断中国的航班，第一个在机场测温，第一个禁止其他国家国民入境，第一个封城 ...  但是，这并没有阻挡疫情爆发...  这些法国都没有做，因为法国政府听取（国际）医疗界的专"})
print(res.text)