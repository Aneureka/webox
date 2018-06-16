# -*- coding: utf-8 -*-
"""
微信公众平台 —— 发送模板消息
"""

from flask import current_app
from app.models import V2EXNews, User
from wechatpy.client.api import WeChatMessage
from app.wechat.wechat_sdk import wechat_client
from app.utils.log_util import get_logger

_wechat_message = WeChatMessage(wechat_client)


def send_to_all():
    openids = User.get_all_openid()
    for openid in openids:
        send_bbs_news_to(openid)
    get_logger().info('sent messages to {NUM} users' . format(NUM=len(openids)))


def send_for_test():
    openid = current_app.config['TEST_OPENID']
    send_bbs_news_to(openid)


def send_bbs_news_to(touser):
    today_v2ex_news = V2EXNews.get_today().get('news')
    for news in today_v2ex_news:
        _send_bbs_msg(touser, news.get('title'), news.get('url'), '-- V2EX')


def _send_bbs_msg(touser, title, url, source='未知来源'):
    template_id = current_app.config['BBS_MSG_TEMPLATE']
    data = {
        'source': {'value': source},
        'title': {"value": title, "color": "#173177"}
    }
    _wechat_message.send_template(touser, template_id, data, url)


