# -*- coding: utf-8 -*-
import requests

from util import doubanutil, tools
from verifycode import wordrecognition
from verifycode import identify_code

def comment_topic(topic_url, comment_dict):
    # 在一个帖子下发表回复

    r = requests.post(topic_url, cookies=doubanutil.get_cookies(),
                      data=comment_dict)
    doubanutil.logger.info("in func comment_topic(), " +
                           str(comment_dict) + ", status_code: " + str(r.status_code))
    return r


def make_comment_dict(topic_url, rv_comment):
    # 组装回帖的参数
    from nltk.corpus import words
    pic_url, pic_id = doubanutil.get_verify_code_pic(topic_url)
    verify_code = ""
    while verify_code =='':
        if len(pic_url):
            verify_codeinword = False
            pic_path = tools.save_pic_to_disk(pic_url)
            rebuild_path=identify_code.recognize_url(pic_path)
            verify_code = wordrecognition.get_word_in_pic(rebuild_path)
            verify_code.replace('/','l')
            verify_code.replace('!', 'i')
            verify_code.replace(' ', '')
            verify_code.replace('.', '')
            if len(verify_code)>=4:
                if verify_code in words.words() or verify_code.lower() in words.words():
                    comment_dict = {
                        "ck": doubanutil.get_form_ck_from_cookie(),
                        "rv_comment": rv_comment,
                        "start": 0,
                        "captcha-solution": verify_code,
                        "captcha-id": pic_id,
                        "submit_btn": "发送"
                    }
                    verify_codeinword = True
                    return comment_dict
                else:
                    pic_url, pic_id = doubanutil.get_verify_code_pic(topic_url)
                    print(pic_url)
                    verify_code = ""
            else:
                pic_url, pic_id = doubanutil.get_verify_code_pic(topic_url)
                print(pic_url)
                verify_code = ""

        comment_dict = {
            "ck": doubanutil.get_form_ck_from_cookie(),
            "rv_comment": rv_comment,
            "start": 0,
            "captcha-solution": verify_code,
            "captcha-id": pic_id,
            "submit_btn": "发送"
        }
    return comment_dict
