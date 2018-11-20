# -*- coding: utf-8 -*

# 카카오플러스 기본 UI 구현하기
from flask import Flask, request, jsonify, json

app = Flask(__name__)


@app.route("/keyboard")
def Keyboard():

    response = {
        "message" : {
            "text" : "원하시는 버튼을 눌러주세요."
        },ㅣ
        "type" : "buttons",
        "buttons" : ["홈으로"]
    }
    return jsonify(response)


@app.route("/message", methods=["POST"])
def message():
    data = json.loads(request.data)
    content = data["content"]

    if content == u"홈으로":
        response = {
            "message" : {
                "text" : "원하시는 정보 버튼을 눌러주세요."
            },
            "keyboard" : {
                "type": "buttons",
                "buttons": ["학원소개", "시간표", "홈으로"]
            }
        }

    # 기본버텬으로 보여주기
    elif content == u"학원소개":
        response = {
            "message" : {
                "text": "우리는 인공지능 기술을 교육합니다."
            },
            "keyboard" : {
                "type" : "buttons",
                "buttons" : ["홈으로"]
            }
        }

    # 이미지와 외부 URL 링크 보여주기
    elif content == u"시간표":
        response = {
            "message" : {
                "text" : "시간표입니다.",
                "photo" : {
                    "url" : "http://twinkleballet.co.kr/data/designImages/BANNER1_1461112781_%EC%8B%9C%EA%B0%84%ED%91%9C.jpg",
                    "width" : 640,
                    "height" : 480
                },
                "message_button" : {
                    "label" : "웹에서 시간표 보기",
                    "url" : "https://www.ai-academy.ai/ai-b2c"
                }
            },
            "keyboard" : {
                "type" : "buttons",
                "buttons" : ["홈으로"]
            }
        }

    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
