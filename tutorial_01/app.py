# -*- coding: utf-8 -*

# 카카오플러스 기본 UI 구현하기
from flask import Flask, request, jsonify, json

app = Flask(__name__)


# [Home Keyboard API]
# 이용자가 최초로 채팅방에 들어올 때 기본으로 키보드 영역에
# 표시될 자동응답 명령어의 목록을 호출하는 API입니다.
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

# [메시지 수신 및 자동응답 API]
# 사용자가 선택한 명령어를 파트너사 서버로 전달하는 API
# 자동응답 명령어에 대한 답변은 응답 메시지(Message)와
# 응답 메시지에 따른 키보드 영역의 답변 방식(Keyboard)의 조합으로 이루어짐
# 답변 방식은 주관식(text)과 객관식(buttons) 중 선택할 수 있음
@app.route("/message", methods=["POST"])
def message():
    data = json.loads(request.data)
    content = data["content"]

    # 기본 버튼 UI
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

    # 기본 버튼 UI
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
