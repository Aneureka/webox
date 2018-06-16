# -*- coding: utf-8 -*-
"""
微信公众平台 —— 管理微信公众平台SDK，自动更新access_token等
"""

from wechatpy.client import WeChatClient
from wechatpy.session.redisstorage import RedisStorage
from redis import Redis

from app.utils.conf_util import get_value

_redis_client = Redis.from_url('redis://127.0.0.1:6379/0')

_session_interface = RedisStorage(
    _redis_client,
    prefix="wechatpy"
)

wechat_client = WeChatClient(
    appid=get_value('wechat', 'appid'),
    secret=get_value('wechat', 'appsecret'),
    session=_session_interface
)

