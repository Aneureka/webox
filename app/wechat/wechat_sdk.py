# -*- coding: utf-8 -*-

import os
from wechatpy.client import WeChatClient
from wechatpy.session.redisstorage import RedisStorage
from redis import Redis

_redis_client = Redis.from_url('redis://127.0.0.1:6379/0')

_session_interface = RedisStorage(
    _redis_client,
    prefix="wechatpy"
)

wechat_client = WeChatClient(
    appid=os.environ.get('APPID'),
    secret=os.environ.get('APPSECRET'),
    session=_session_interface
)

