# -*- coding: utf-8 -*

# Helloworld 으로 시작하기
from flask import Flask, jsonify

# Flask 인스턴스를 생성하여 app 에 할당
# __name__ 은 모듈이름을 가지고 있는 내장변수
app = Flask(__name__)


# 서버 정상 동작여부를 파악하기 위한 테스트 route
@app.route("/")
def hello_world():
    return "Hello, World!"


# [Home Keyboard API]
# 이용자가 최초로 채팅방에 들어올 때 기본으로 키보드 영역에
# 표시될 자동응답 명령어의 목록을 호출하는 API입니다.
# 챗팅방을 지우고 다시 재 진입시에도 호출됩니다.
@app.route("/keyboard")
def keyboard():

    # Flask에서는 jsonify라는 유틸리티 함수가 있어서
    # dictionary이나 배열을 던져서 쉽게 JSON 타입의의
    # HTTP Response를 생성해준다
    return jsonify(type="text")


# [메시지 수신 및 자동응답 API]
# 사용자가 선택한 명령어를 파트너사 서버로 전달하는 API
# 자동응답 명령어에 대한 답변은 응답 메시지(Message)와
# 응답 메시지에 따른 키보드 영역의 답변 방식(Keyboard)의 조합으로 이루어짐
# 답변 방식은 주관식(text)과 객관식(buttons) 중 선택할 수 있음
@app.route("/message", methods=["POST"])
def message():
    response = {
        "message": {
            "text": "Hello, World!"
        }
    }

    return jsonify(response)


# if __name__ == ""__main__""은 왜 쓰는건가요?
#
# 모듈이 직접 실행되는 경우(python app.py)에만,
# __name__ 은 "__main__"으로 설정
# 즉, 스크립트가 직접 실행되는경우만 실행
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
