# -*- coding: utf-8 -*-
import random
import time
import requests
from lxml import etree

from group import comment
from config import doubanurl
from util import doubanutil

if __name__ == "__main__":
    # group_id = "hezu"
    # group_url = doubanurl.DOUBAN_GROUP + group_id
    # r = requests.get(group_url, cookies=doubanutil.get_cookies())
    # group_topics_html = etree.HTML(r.text)
    # group_topics = group_topics_html.xpath(
    #     "//table[@class='olt']/tr/td[@class='title']/a/@href")
    # group_topics = group_topics[5:]
    group_topics=['https://www.douban.com/group/topic/114428461/',
                  'https://www.douban.com/group/topic/114428619/',
                  'https://www.douban.com/group/topic/114428544/',
                  'https://www.douban.com/group/topic/114429175/',
                  'https://www.douban.com/group/topic/114428903/',]
    while True:
        try:
            for topic_url in group_topics:
                comment_topic_url = topic_url + "/add_comment#last"
                comment_str = "顶起来"
                comment_dict = comment.make_comment_dict(topic_url, comment_str)
                if comment_dict == False :
                    continue
                comment.comment_topic(comment_topic_url, comment_dict)
                random_sleep = random.randint(60, 100)
                time.sleep(random_sleep)
            random_sleep = random.randint(300, 500)
        except:
            print(topic_url+'not comment')


