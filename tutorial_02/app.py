# !/usr/bin/python
# -*- coding: utf-8 -*

from flask import Flask, request, jsonify, json
from openpyxl import load_workbook, cell

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

EXCEL_FILE_NAME = 'Database.xlsx'
db = load_workbook(filename=EXCEL_FILE_NAME)
user_db = db['User']


@app.route("/")
def say_hi():
    return "안녕하세요. 아카데미의 챗봇입니다."


@app.route("/keyboard")
def Keyboard():

    response = {
        "message" : {
            "text" : "원하시는 버튼을 눌러주세요."
        },
        "type" : "buttons",
        "buttons" : ["홈으로"]
    }
    return jsonify(response)


@app.route("/message", methods=["POST"])
@app.route("/message", methods=["GET"])
def message():
    data = json.loads(request.data)
    content = data["content"]
    user_key = data["user_key"]

    for idx, row in enumerate(user_db.rows):
        if idx != 0 and row[0].value == user_key:
            print('기존 사용자', row)
            user_row = row
            break

        if idx == user_db.max_row - 1:
            print('새로운 사용자', row)
            NEW_INDEX = user_db.max_row + 1
            user_db[NEW_INDEX][0].value = user_key
            user_db[NEW_INDEX][1].value = 0
            db.save(EXCEL_FILE_NAME)
            user_row = user_db[user_db.max_row]

            response = {
                "message" : {
                    "text" : "처음 오셨네요? 이름이 뭐에요?"
                },
                "keyboard" : {
                    "type": "text"
                }
            }
            return jsonify(response)

    if user_row[1].value is 0:
        user_row[1].value = 1
        user_row[2].value = content
        db.save(EXCEL_FILE_NAME)

        response = {
            "message" : {
                "text" : "{name}님, 반갑습니다.".format(name=content)
            },
            "keyboard" : {
                "type": "buttons",
                "buttons": ["학원소개", "시간표", "홈으로"]
            }
        }

        return jsonify(response)

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
    app.run(host='0.0.0.0', port=5000, debug=True)
