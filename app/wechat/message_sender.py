# -*- coding: utf-8 -*-
"""
微信公众平台 —— 发送模板消息
"""

import requests
import json
from flask import current_app
from app.models import V2EXNews, User
from app.wechat.access_token_helper import get_access_token


def send_to_all():
    openids = User.get_all_openid()
    for openid in openids:
        send_bbs_news_to(openid)


def send_bbs_news_to(touser):
    today_v2ex_news = V2EXNews.get_ystd().get('news')
    print(today_v2ex_news)
    for news in today_v2ex_news:
        _send_bbs_msg(touser, news.get('title'), news.get('url'), 'v2ex')


def _send_bbs_msg(touser, title, url, source='未知来源'):
    template_id = current_app.config['BBS_MSG_TEMPLATE']
    data = {
        'source': {'value': source},
        'title': {"value": title, "color": "#173177"}
    }
    _send_msg(touser, template_id, url, data)


def _send_msg(touser, template_id, url, data):
    access_token = get_access_token()
    to_url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={ACCESS_TOKEN}' . format(ACCESS_TOKEN=access_token)
    msg = {'touser': touser, 'template_id': template_id, 'url': url, 'data': data}
    ret_content = json.loads(requests.post(to_url, json.dumps(msg)).content.decode('utf-8'))
    if not ret_content or ret_content.get('errcode') != 0:
        print('发送失败！')


