from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException 
from tencentcloud.nlp.v20190408 import nlp_client, models 
try: 
    cred = credential.Credential("AKIDd3KTQBKyE2teIkGar13oQwLcq24wctXC", "R3gAVglzFC51wkQwPuNhrpgBYjYYcbTX") 
    httpProfile = HttpProfile()
    httpProfile.endpoint = "nlp.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile) 

    req = models.KeywordsExtractionRequest()
    params = '{"Text":"被问及法国为什么不采取意大利式的封锁，法国政府发言人 NDIAYE 公开蔑视意大利政府的措施：在欧洲，他们第一个中断中国的航班，第一个在机场测温，第一个禁止其他国家国民入境，第一个封城 ...  但是，这并没有阻挡疫情爆发...  这些法国都没有做，因为法国政府听取（国际）医疗界的专"}'
    req.from_json_string(params)

    resp = client.KeywordsExtraction(req) 
    print(resp.to_json_string()) 

except TencentCloudSDKException as err: 
    print(err) 
