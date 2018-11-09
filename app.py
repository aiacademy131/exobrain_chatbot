# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, json
from openpyxl import load_workbook
import json
#from button_answer import button_answer
from excel_answer import excel_answer
from excel_db import *
from data_send import *

app = Flask(__name__)
db = load_workbook(filename='Database.xlsx')
user_db = db['User_data']  #Sheet 설정


@app.route("/")
def say_hi():
    return "안녕하세요? 한국인공지능아카데미 개시했습니다. 저는 문아라입니다."


# @app.route("/keyboard")
# def Keyboard():
#
#     dataSend = {
#         "message" : {
#             "text" : "안녕하세요. 인공지능 아카데미입니다. 원하시는 버튼을 눌러주세요."
#         },
#         "type" : "buttons",
#         "buttons" : ["홈으로"]
#     }
#     return jsonify(dataSend)

@app.route("/message", methods=["POST"])
def Message():

    data = json.loads(request.data)
    content = data["content"]
    user_key = data["user_key"]
    user_row = find_user_row(user_key)

    try:
        response = jsonify(excel_answer(content, user_row))


    except :
        response = jsonify(data_send.return_buttons("잘못된 접근이에요. 처음으로 돌아갈께요","홈으로"))

    return response


@app.route("/friend", methods=["DELETE"])
# 사용자가 친구삭제를 했을때 커스텀된 데이터는 지워야한다.
def friend_out():
    data = json.loads(request.data)
    user_row = find_user_row(data["user_key"])
    delete_userdata(user_row)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
