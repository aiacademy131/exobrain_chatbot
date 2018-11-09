# !/usr/bin/python
# -*- coding: utf-8 -*

from flask import Flask, request, jsonify, json
from openpyxl import load_workbook, cell
import excel_db

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

EXCEL_FILE_NAME = 'Database.xlsx'
db = load_workbook(filename=EXCEL_FILE_NAME)

user_db = db['User_data']
answer_db = db['Answer']


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
    user = excel_db.get_user_row(user_key)

    response = excel_db.get_response(content)

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
