import urllib3
import json

openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU"
accessKey = "4ee51c5e-7d13-4f91-9516-5f68c4fe26f3"

# [AnaylsisCode]
# morp - 형태소 분석 / wsd - 어휘 의미 분석(동음이의) / wsd_poly - 어휘 의미 분석(다의)
# ner - 개체명 인식 / dparse - 의존 구문 / srl - 의미역
def exobrainNLU(type, sentence):
    analysisCode = type
    requestJson ={
        "access_key" : accessKey,
        "argument" : {
            "text" : sentence,
            "analysis_code" : analysisCode
        }
    }

    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body = json.dumps(requestJson, indent= 2)
    )


    data = json.loads(response.data.decode('utf-8'))

    #type Dic 형태를 list로 전환해서 return
    return list(data["return_object"]['sentence'])
