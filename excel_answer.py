import itertools
from openpyxl import load_workbook
from flask import jsonify
from excel_db import *
from data_send import *
from bayesian import Filter
from Text_Analysis import keyword_check

db = load_workbook(filename='Database.xlsx')
answer_db = db['Answer']
dataSend = {}
MSG_KEYWORD = ["text","text_Function"]
RES_KEYWORD = ["buttons", "text", "buttons_url", "buttons_pic", "buttons_Function","buttons_url_Function"]
TRIGGER_KEYWORD_01 = "홈으로"  # Queston Depth 초기화
TRIGGER_KEYWORD_02 = ["수업소개","설명회"] # Topic 변수 트리거
TRIGGER_KEYWORD_03 = ['설명회 주제','강의 정보','강의 세부 정보'] # Python Function to Buttons
TRIGGER_KEYWORD_04 = ['사용자 질문 분석','설명회 내용'] # Python Function to Message
TRIGGER_KEYWORD_05 = ['고등학생','아니오']  # Question_Depth Trigger
USERINFO_KEYWORD = {"직업" : ["학생","직장인"],"학력" :["대학생 이상","고등학생"],"대답" : ["네","아니오"]}


def excel_answer(content, user_row):            # user_row ==> user
    global dataSend
    # print("Question_Depth :")
    # print(return_question_depth(user_row))

    if content == TRIGGER_KEYWORD_01:
        initalize_question_depth(user_row, 0)
        data = excel_ui(content)
        dataSend = data_send.return_buttons(data[3],data[5].split(","))

    elif return_question_depth(user_row) == 1:
        if content in contents_list(return_question_depth(user_row)):
            dataSend = simple_answer(content, user_row)
            if content in TRIGGER_KEYWORD_02:
                user_topic = TRIGGER_KEYWORD_02[TRIGGER_KEYWORD_02.index(content)]
                save_user_topic(user_row, user_topic)

    elif return_question_depth(user_row) == 2:        #사용자 맞춤형 질문
        if content in contents_list(return_question_depth(user_row)):
            dataSend = simple_answer(content, user_row)

        elif content in question_info(return_question_depth(user_row)):
            dataSend = simple_answer(content,user_row)

        elif "[" in content:
            dataSend = data_send.return_buttons("설명회 주제 하단에 있는 항목을 눌러주세요",seminar_topic())
            return dataSend

        elif content in seminar_topic():
            dataSend = data_send.return_buttons(seminar_info(content),["상담 예약하기","홈으로"])
            initalize_question_depth(user_row, 7)
            return dataSend

        else:
            dataSend = bayesian_filter(content)

    elif return_question_depth(user_row) == 3:
        if content in contents_list(return_question_depth(user_row)):
            dataSend = simple_answer(content, user_row)

        elif content in question_info(3):
            dataSend = simple_answer(content, user_row)

        elif content in lecture_info():
            dataSend = data_send.return_buttons(detail_lecture_info(content), ["상담 예약하기", "홈으로"])
            initalize_question_depth(user_row, 7)
            return dataSend

    elif return_question_depth(user_row) in range(4, 7):

        if return_question_depth(user_row) == 6:
            text = "제가 사용자님에게 어울릴만한 목록을 뽑아봤어요!"
            buttons = custom_lecture_info(user_row)
            dataSend = data_send.return_buttons(text, buttons)
            next_question_depth(user_row)
            return dataSend

        elif content in contents_list(return_question_depth(user_row)):
            dataSend = simple_answer(content, user_row)

        elif content in lecture_info():
            dataSend = data_send.return_buttons(lecture_info(content), ["상담 예약하기", "홈으로"])
            initalize_question_depth(user_row, 7)
            return dataSend

        userType = return_user_type(user_row)
        #save_answer_data(content, return_question_depth(user_row), user_row)  # 4 네
        text = question_msg(userType, return_question_depth(user_row))  # 4 #5
        buttons = ["네","아니오"]
        dataSend = data_send.return_buttons(text, buttons)

    elif return_question_depth(user_row) == 7:
        if content == "상담 예약하기":
            dataSend = data_send.return_message("예약가능하신 장소와 날짜 시간을 입력해주세요")

        elif content in lecture_info():
            dataSend = data_send.return_buttons(detail_lecture_info(content),["상담 예약하기","홈으로"])
            return dataSend

    elif return_question_depth(user_row) == 8:

        keyword_sentence = []
        keyword_sets = keyword_check(content)
        for k in range(len(keyword_sets)):
            keyword_text = "".join(keyword_sets[k][1]) + " : " + "".join(keyword_sets[k][0]) + "\n"
            print(keyword_text)
            keyword_sentence.append(keyword_text)
        dataSend = data_send.return_buttons("".join(keyword_sentence),["맞습니다","아니에요 수정할께요"])
        next_question_depth(user_row)
        return dataSend


    elif return_question_depth(user_row) == 9:
        if content == '맞습니다':
            dataSend = data_send.return_buttons("END",["홈으로"])

        elif content == '아니에요 수정할께요':
            print("1")
            dataSend = data_send.return_message("예약 가능한 시간과 장소를 다시 말해주세요")
            initalize_question_depth(user_row, 8)
            return dataSend
    #Question_depth control



    if  content in list(itertools.chain.from_iterable(USERINFO_KEYWORD.values())):
        save_answer_data(content, return_question_depth(user_row), user_row)

    if content in TRIGGER_KEYWORD_05:
        initalize_question_depth(user_row, 6)
    elif content == "학원소개":
        initalize_question_depth(user_row, 1)
    else:
        next_question_depth(user_row)

    # print("output QD :")
    # print(return_question_depth(user_row))
    return dataSend

# request 값과 일치하는 content를 buttons 형식을 기준으로 response
def simple_answer(content, user_row):
    global dataSend

    data = excel_ui(content)  # Excel Answer Sheet에서 data 추출       // 단순 질의문
    #print(data)
    # buttons
    if data[4] == RES_KEYWORD[0]:
        dataSend = data_send.return_buttons(data[3], data[5].split(","))
        if data[4] == TRIGGER_KEYWORD_01:
            initalize_question_depth(user_row, 0)
    # text
    elif data[4] == RES_KEYWORD[1]:
        dataSend = data_send.return_message(data[3])
    # buttons with url
    elif data[4] == RES_KEYWORD[2]:
        dataSend = data_send.return_buttons_with_url(data[3], data[5].split(","), data[6], data[7])
    # buttons with pic

    elif data[4] == RES_KEYWORD[3]:
        dataSend = data_send.return_buttons_with_pic(data[3], data[5].split(","), data[8], data[6], data[7])

    # Python Function Buttons
    elif data[4] == RES_KEYWORD[4]:
        for idx in range(len(TRIGGER_KEYWORD_03)):
            if data[5].split(" : ")[1] == TRIGGER_KEYWORD_03[idx]:
                if idx == 0:
                    buttons = seminar_topic()
                elif idx == 1:
                    buttons = lecture_info()
        dataSend = data_send.return_buttons(data[3], buttons)

    elif data[4] == RES_KEYWORD[5]:
        for idx in range(len(TRIGGER_KEYWORD_03)):
            if data[5].split(" : ")[1] == TRIGGER_KEYWORD_03[idx]:
                if idx == 0:
                    buttons = seminar_topic()
                elif idx == 1:
                    buttons = lecture_info()
        dataSend = data_send.return_buttons_with_url(data[3], buttons, data[6], data[7])
    return dataSend

# 베이지안 필터
def bayesian_filter(content):

    bf = Filter()
    b_data = lecture_info("bayesian")

    for i in range(len(b_data)):  # filter fitting 과정
        for k in range(len(b_data[i][1][:-1])):
            bf.fit(b_data[i][1][k], b_data[i][0])

    pre, scorelist = bf.predict(content)
    buttons = lecture_info(pre) + ["모든 수업 보기"]
    text = "여기 제가 생각해본 사용자님과 맞는 " + pre + " 수업목록이에요. 모든 수업을 보고싶으시면 모두보기를 눌러주세요."
    dataSend = data_send.return_buttons(text, buttons)

    return dataSend

