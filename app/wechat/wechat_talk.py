# -*- coding: utf-8 -*-

import os
import re
from flask import jsonify
from app.models import InternshipNews
from wechatpy.client.api import WeChatMessage
from app.wechat.wechat_sdk import wechat_client
from app.utils.log_util import get_logger
from wechatpy.replies import TextReply
from wechatpy.messages import *
from wechatpy.events import *

_wechat_message = WeChatMessage(wechat_client)


def _default_text_reply_content():
    return '还没想好怎么回答这个问题QAQ'


NEWS_PATTERNS = {
    'today_internship': '今.*实习',
    'ystd_internship': '昨.*实习',
    'internship': '实习'
}

MESSAGES = {
    'subscribe': '感谢小改改的关注~[Hey]\n试着用下公众号吧~比如可以试试 实习、今天的实习、昨天实习 之类的~',
    'default': '试着用下公众号吧~可以试试 实习、今天的实习、昨天实习 之类的~'
}


def dispose_message(msg):
    # respond to message
    if isinstance(msg, BaseEvent):
        if isinstance(msg, SubscribeEvent):
            get_logger().info('be subscribed by ' + msg.source)
            return TextReply(content=MESSAGES['subscribe'], message=msg)
        else:
            return TextReply(content=MESSAGES['default'], message=msg)
    else:
        if isinstance(msg, TextMessage):
            get_logger().info('receive message: ' + msg.content)
            return TextReply(content=dispose_text_message(msg), message=msg)
        elif isinstance(msg, VoiceMessage):
            return TextReply(content=MESSAGES['default'], message=msg)
        else:
            return TextReply(content=MESSAGES['default'], message=msg)


def dispose_text_message(msg):
    content = msg.content
    if _matches(content, NEWS_PATTERNS['today_internship']):
        return InternshipNews.to_text(InternshipNews.get_today())
    elif _matches(content, NEWS_PATTERNS['ystd_internship']):
        return InternshipNews.to_text(InternshipNews.get_ystd())
    elif _matches(content, NEWS_PATTERNS['internship']):
        return InternshipNews.to_text(InternshipNews.get_latest())
    else:
        return MESSAGES['default']



def _matches(text, pat):
    p = re.compile(pat)
    return len(p.findall(text)) > 0


def get_func(message):
    content = message.content
    for p, f in NEWS_PATTERNS.items():
        pat = re.compile(p)
        res = re.findall(pat, content)
        if len(res) > 0:
            return f
    return _default_reply


