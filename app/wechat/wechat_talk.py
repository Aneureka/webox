# -*- coding: utf-8 -*-

import re
from wechatpy.replies import TextReply, MusicReply
from wechatpy.messages import *
from wechatpy.events import *

from app.models import InternshipNews, Feedback
from wechatpy.client.api import WeChatMessage
from app.wechat.wechat_sdk import wechat_client
from app.utils.log_util import get_logger
from app.spiders.eecs_pku_spider import fetch_eecs_pku


_wechat_message = WeChatMessage(wechat_client)


def _default_text_reply_content():
    return '还没想好怎么回答这个问题QAQ'


MSG_PATTERNS = {
    'internship': '实习',
    'feedback': '\/\:\:\)',
    'pku_eecs': '信科院'
}


INTERNSHIP_PATTERNS = {
    'today': '今天',
    'ystd': '昨天',
    'source': '\*(\S+)\*',
    'company': '\+(\S+)\+',
    'address': '\-(\S+)\-',
    'default': '.*',
}

MESSAGES = {
    'subscribe': '感谢小改改的关注[Hey]\n可以试试【实习】、【今天的实习】、【昨天实习】之类的命令，会做出更好用的功能的~',
    'default': '/:shake现在支持的指令/:shake\n1. 实习\n2. 今天的实习\n3. 昨天的实习\n4. +公司名+实习\n5. -城市-实习\n6. *来源*实习\n如果想要吐槽或建议，只要在建议里面加个表情/::)就可以啦hhh\n',
    'no_internship': '哎呀，现在还没有想要的实习呢~',
    'feedback': '阿里嘎多[Hey]\n在下已经记住啦！'
}


def dispose_message(msg):
    # respond to message
    if isinstance(msg, BaseEvent):
        if isinstance(msg, SubscribeEvent):
            get_logger().info('be subscribed by: ' + msg.source)
            return TextReply(content=MESSAGES['subscribe'], message=msg)
        elif isinstance(msg, UnsubscribeEvent):
            get_logger().info('be unsubscribed by: ' + msg.source)
        else:
            get_logger().info('undefined event: ' + msg.event)
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
    if _matches(content, MSG_PATTERNS['internship']):
        if _matches(content, INTERNSHIP_PATTERNS['today']):
            return InternshipNews.to_text(InternshipNews.get_today())
        elif _matches(content, INTERNSHIP_PATTERNS['ystd']):
            return InternshipNews.to_text(InternshipNews.get_ystd())
        elif _matches(content, INTERNSHIP_PATTERNS['company']):
            company = _get_keyword(content, INTERNSHIP_PATTERNS['company'])
            return InternshipNews.to_text(InternshipNews.get_by_company(company))
        elif _matches(content, INTERNSHIP_PATTERNS['address']):
            address = _get_keyword(content, INTERNSHIP_PATTERNS['address'])
            return InternshipNews.to_text(InternshipNews.get_by_company(address))
        elif _matches(content, INTERNSHIP_PATTERNS['source']):
            source = _get_keyword(content, INTERNSHIP_PATTERNS['source'])
            return InternshipNews.to_text(InternshipNews.get_by_source(source))
        else:
            return InternshipNews.to_text(InternshipNews.get_latest())

    elif _matches(content, MSG_PATTERNS['pku_eecs']):
        return fetch_eecs_pku()

    elif _matches(content, MSG_PATTERNS['feedback']):
        Feedback.add(Feedback(source=msg.source, content=msg.content))
        return MESSAGES['feedback']

    else:
        return MESSAGES['default']


def _matches(text, pat):
    p = re.compile(pat)
    return len(p.findall(text)) > 0

def _get_keyword(text, pat):
    p = re.compile(pat)
    return p.match(text).group(1)


