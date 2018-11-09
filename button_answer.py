# from flask import jsonify
# from excel_db import *
# from bayesian import Filter
# from data_send import *
#
# dataSend = {}
#
#
# def button_answer(content, userKey):
#     print(return_question_depth(userKey))
#
#     if content == "학원소개":
#         text = "우리는 인공지능 기술을 교육합니다.\n시대는 너무나 빠르게 변화하고 있고, 인공지능은 우리 삶에 현실로 들어오고 있습니다.\n인공지능 기술을 누구나 알고 이해하고 쉽게 쓸 수 있도록 우리는 인공지능 기술을 교육합니다."
#         label = "웹에서 소개 보기"
#         url = "https://www.ai-academy.ai/academics"
#         buttons = ["수업소개","오시는길","홈으로(버튼)","홈으로(엑셀)"]
#         dataSend = data_send.return_buttons_with_url(text, buttons, label, url)
#
#
#     elif content == "오시는길":
#         text = "서울특별시 중구 한강대로 416\n서울스퀘어 위워크"
#         buttons = ["홈으로(버튼)"]
#         pic_url = "https://www.ai-academy.ai/contact"
#         buttons_label = "웹에서 지도보기"
#         buttons_url = "https://www.ai-academy.ai/contact"
#         dataSend = data_send.return_buttons_with_pic(text, buttons, pic_url, buttons_label,buttons_url)
#
#     elif content == "홈으로(버튼)":
#         initalize_question_depth(userKey, 0)  # 0 #처음에서는 depth를 초기화
#         print(userDB[userDB.max_row][0].value)
#         text = "원하시는 정보를 눌러주세요"
#         buttons = ["학원소개","수업소개","설명회","홈으로(버튼)","홈으로(엑셀)"]
#         dataSend = data_send.return_buttons(text, buttons)
#         next_question_depth(userKey) # 1
#
#     # 전체 설명회 데이터를 제시 case photo
#     elif content == "설명회":
#         text = "설명회 일정입니다"
#         buttons = seminar_topic()
#         pic_url = "https://dc.mirae-academy.co.kr/wp-content/uploads/sites/53/2018/08/8%EC%9B%94%ED%95%99%EB%B6%80%EB%AA%A8%EB%8B%98-%EC%B4%88%EB%8C%80_%EC%88%98%EC%A0%95%EB%B3%B85.jpg"
#         buttons_label = "웹에서 일정표 보기"
#         buttons_url = "https://www.ai-academy.ai/ai-b2c"
#         dataSend = data_send.return_buttons_with_pic(text, buttons, pic_url, buttons_label, buttons_url)
#
#         next_question_depth(userKey)
#
#     # 설명회 주제 선택 버튼 --> 세부내용
#     elif content in seminar_topic():
#         text = seminar_info(content)
#         buttons = ["상담 예약하기","뒤로가기","홈으로"]
#         dataSend = data_send.return_buttons(text, buttons)
#         initalize_question_depth(userKey, 7)
#
#
#     elif content == "수업소개":
#         text = "앗! 잠깐만요. 제가 사용자님이 어디에 관심있는지 얘기해주시면 맞춤형 강좌를 추천해드릴수있어요!\n잘 모르겠으면 제가 질문을 드려도 될까요?"+\
#                "제 질문을 원하시면 <질문해줘>라고 얘기해주세요\n대답을 원치 않으시면 <모두보기>라고 얘기해주세요"
#         dataSend = data_send.return_message(text)
#
#         next_question_depth(userKey) # 2
#
#
#     elif return_question_depth(userKey) == 2:
#         if content == "모두보기":
#             text = "모든 강좌정보 입니다. 관심있는 강좌명을 눌러주세요"
#             buttons = lecture_info(None)
#             dataSend = data_send.return_buttons(text, buttons)
#
#
#         elif content == "질문해줘":
#             text = "대학교를 졸업하셨나요?"
#             buttons = ["네", "아니오"]
#             dataSend = data_send.return_buttons(text, buttons)
#
#
#         else:   #Baysian Filter with Exobrain API
#             bf = Filter()
#             b_data = lecture_info("bayesian")
#
#             for i in range(len(b_data)):        #filter fitting 과정
#                 for k in range(len(b_data[i][1][:-1])):
#                     bf.fit(b_data[i][1][k],b_data[i][0])
#
#
#             pre, scorelist = bf.predict(content)
#             print(pre)
#             buttons = lecture_info(pre) + ["모두보기"]
#             text = "여기 제가 생각해본 사용자님과 맞는 " + pre + " 수업목록이에요. 모든 수업을 보고싶으시면 모두보기를 눌러주세요."
#             dataSend = data_send.return_buttons(text, buttons)
#
#         next_question_depth(userKey)#3
#
#
#     elif return_question_depth(userKey) == 3:
#         if content == "아니오":
#             text = question_msg("학생", return_question_depth(userKey))
#             buttons = ["네","아니오"]
#             dataSend = data_send.return_buttons(text, buttons)
#             save_answer_data("학생", return_question_depth(userKey), userKey)  # 3
#             next_question_depth(userKey)  # 4
#
#         elif content == "네":
#             print("100")
#             text = question_msg("성인", return_question_depth(userKey))
#             save_answer_data("성인", return_question_depth(userKey), userKey)
#             buttons = ["네","아니오"]
#             dataSend = data_send.return_buttons(text, buttons)
#             next_question_depth(userKey)  #4
#
#         elif content == "모두보기":
#             text = "모든 강좌정보 입니다. 관심있는 강좌명을 눌러주세요"
#             buttons = lecture_info(None)
#             dataSend = data_send.return_buttons(text, buttons)
#             initalize_question_depth(userKey, 6)
#
#         else:
#             initalize_question_depth(userKey, 7)
#             text = detail_lecture_info(content)
#             buttons = ["상담 예약하기", "홈으로(버튼)", "홈으로(엑셀)"]
#             dataSend = data_send.return_buttons(text, buttons)
#             return jsonify(dataSend)
#
#             next_question_depth(userKey)
#
#     elif return_question_depth(userKey) in range(4, 6):
#         save_answer_data(content, return_question_depth(userKey), userKey) #4 네
#         if return_question_depth(userKey) == 6:
#             text = "제가 사용자님에게 어울릴만한 목록을 뽑아봤어요!"
#             buttons = custom_lecture_info(userKey)
#             dataSend = data_send.return_buttons(text, buttons)
#
#             return jsonify(dataSend)
#
#         userType = return_user_type(userKey)
#         print(content, return_question_depth(userKey),userType)
#         print(question_msg(userType,return_question_depth(userKey)))
#         text = question_msg(userType, return_question_depth(userKey))  #4 #5
#         buttons = ["네","아니오"]
#         dataSend = data_send.return_buttons(text, buttons)
#
#         next_question_depth(userKey) #5 #6
#         print(content, return_question_depth(userKey))
#
#
#
#     elif content == "상담 예약하기":
#         dataSend = data_send.return_message("원하시는 날짜, 장소, 시간을 얘기해주세요.")
#
#
#     elif content in lecture_info(None):
#         initalize_question_depth(userKey, 7)
#         text = detail_lecture_info(content)
#         print(text)
#         buttons = ["상담 예약하기","홈으로(버튼)","홈으로(엑셀)"]
#         dataSend = data_send.return_buttons(text, buttons)
#         print(dataSend)
#
#         next_question_depth(userKey) #8
#
#     elif return_question_depth(userKey) == 8:
#         return 0
#
#     return jsonify(dataSend)
