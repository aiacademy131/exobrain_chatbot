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


# Home Keyboard API
# 이용자가 최초로 채팅방에 들어올 때 기본으로 키보드 영역에
# 표시될 자동응답 명령어의 목록을 호출하는 API입니다.
# 챗팅방을 지우고 다시 재 진입시에도 호출됩니다.
# 다만 카카오 서버에서도 1분동안 캐쉬가 저장되기 때문에 유저가 채팅방을 지우고
# 들어오는 행동을 반복하더라도 개발사 서버를 1분에 한번씩 호출하게 됩니다.
# 즉, 개발사 서버에서 정보가 변경되어도 최대 1분뒤에 유저들에게 반영이 됩니다.
# 유저가 자동응답으로 메시지를 주고 받았을 경우는 마지막 메시지에 담겨있던
# 자동응답 명령어 목록이 표시됩니다.
# 다만 메시지에 저장된 자동응답 명령어는 10분간 유효합니다.
# 10분이 지난 다음에는 다시 keyboard api를 호출하여
# 자동응답 목록을 초기화하게 됩니다.
@app.route("/keyboard")
def keyboard():
    return jsonify(type="text")


# 메시지 수신 및 자동응답 API
# 사용자가 선택한 명령어를 파트너사 서버로 전달하는 API
# 자동응답 명령어에 대한 답변은 응답 메시지(Message)와
# 응답 메시지에 따른 키보드 영역의 답변 방식(Keyboard)의 조합으로 이루어짐
# 답변 방식은 주관식(text)과 객관식(buttons) 중 선택할 수 있음
# 자동응답을 통해 친구에게 미디어 타입(사진/동영상/오디오)을 받고자 하는 경우
# 주관식 키보드(text)를 선택하세요. 메시지를 통해 <‘+’버튼을 눌러
# 미디어를 전송하세요>와 같이 안내하는 것이 필요 할 수 있습니다.
# 유저가 보낸 미디어 타입의 카카오 서버에서의 보존기간은 아래와 같습니다.
# 음성파일 : 20일
# 이미지파일 : 20일
# 비디오 : 20일
# 미디어 파일의 보존기간은 서버의 상황에 의하여 변동 될 수 있습니다.
@app.route("/message", methods=["POST"])
def message():
    response = {
        "message": {
            "text": "Hello, World!"
        }
    }

    return jsonify(response)


# 서버실행
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
