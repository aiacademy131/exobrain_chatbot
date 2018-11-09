import urllib3
import json

openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU"
accessKey = "4ee51c5e-7d13-4f91-9516-5f68c4fe26f3"
# AnaylsisCode = morp - 형태소 분석 / wsd - 어휘 의미 분석(동음이의) / wsd_poly - 어휘 의미 분석(다의)
#                ner - 개채명 인식 / dparse - 의존 구문 / srl - 의미역


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

def keyword_check(sentence):
    keyword_sets = []
    malist = exobrainNLU("ner",sentence)
    #print(malist)
    for i in range(len(malist[0]['NE'])):
        keyword = malist[0]['NE'][i]['text']
        keyword_type = malist[0]['NE'][i]['type']
        print("".join(keyword_type[:2]))
        keyword_type = list(map(lambda x,y : "날짜" if x+y == "DT" else "시간" if x+y == "TI" else "장소" if x+y == "LC" else x+y , keyword_type[0],keyword_type[1]))
        keyword_set = (keyword , keyword_type)
        keyword_sets.append(keyword_set)
    print(keyword_sets)
    return keyword_sets