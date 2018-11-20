# -*- coding: utf-8 -*

# Helloworld 으로 시작하기
from flask import Flask
from flask import jsonify
from flask import json

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/keyboard")
def keyboard():
    return jsonify(type="text")


@app.route("/message", methods=["POST"])
def message():
    response = {
        "message": {
            "text": "Hello, World!"
        }
    }

    response = json.dumps(response, ensure_ascii=False)
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
