# -*- coding: utf-8 -*-
"""
微信公众平台 —— 处理接受消息
"""

from lxml import etree
import time

from flask import current_app


def parse_wechat_data(wechat_data):
    if len(wechat_data) == 0:
        return None
    xml_data = etree.fromstring(wechat_data)
    msg_type = xml_data.find('MsgType').text
    if msg_type == 'text':
        return TextMsg.from_xml(xml_data)
    elif msg_type == 'image':
        return ImageMsg.from_xml(xml_data)
    else:
        return Msg.from_xml(xml_data)


class Msg(object):
    def __init__(self):
        self.ToUserName = ''
        self.FromUserName = ''
        self.CreateTime = int(time.time())
        self.MsgType = 'text'
        self.MsgId = 0

    @staticmethod
    def from_xml(xml_data):
        msg = Msg()
        msg.ToUserName = xml_data.find('ToUserName').text
        msg.FromUserName = xml_data.find('FromUserName').text
        msg.CreateTime = xml_data.find('CreateTime').text
        msg.MsgType = xml_data.find('MsgType').text
        msg.MsgId = xml_data.find('MsgId').text
        return msg

    def render(self):
        return "我已经收到信息啦，但我不知道怎么回复你。你能教教我吗>_<"


class TextMsg(Msg):
    def __init__(self):
        Msg.__init__(self)
        self.Content = ''

    @staticmethod
    def from_xml(xml_data):
        msg = Msg.from_xml(xml_data)
        msg.Content = xml_data.find('Content').text
        return msg

    @staticmethod
    def from_default(to_user_name, from_user_name, content):
        msg = TextMsg()
        msg.ToUserName = to_user_name
        msg.FromUserName = from_user_name
        msg.Content = content
        msg.CreateTime = int(time.time())
        return msg

    def render(self):
        return current_app.config['TEXT_MSG_TEMPLATE'].format(**self.__dict__)


class ImageMsg(Msg):
    def __init__(self):
        Msg.__init__(self)
        self.PicUrl = ''
        self.MediaId = 0

    @staticmethod
    def from_xml(xml_data):
        msg = Msg.from_xml(xml_data)
        msg.PicUrl = xml_data.find('PicUrl').text
        msg.MediaId = xml_data.find('MediaId').text
        return msg

    @staticmethod
    def from_default(to_user_name, from_user_name, media_id):
        msg = ImageMsg()
        msg.ToUserName = to_user_name
        msg.FromUserName = from_user_name
        msg.MediaId = media_id
        msg.CreateTime = int(time.time())
        return msg

    def render(self):
        return current_app.config['IMAGE_MSG_TEMPLATE'].format(**self.__dict__)


class EventMsg(Msg):
    def __init__(self):
        Msg.__init__(self)
        self.Event = ''

    @staticmethod
    def from_xml(xml_data):
        msg = Msg.from_xml(xml_data)
        msg.Event = xml_data.find('Event').text
        return msg

    @staticmethod
    def from_default(event):
        msg = EventMsg()
        msg.Event = event
        return msg

    # todo
    def render(self):
        raise NotImplementedError
