# -*- coding: utf-8 -*-

import os
from wechatpy.client import WeChatClient
from wechatpy.session.redisstorage import RedisStorage
from redis import Redis

__redis_client = Redis.from_url('redis://127.0.0.1:6379/0')

__session_interface = RedisStorage(
    __redis_client,
    prefix="wechatpy"
)

wechat_client = WeChatClient(
    appid=os.environ.get('WEBOX_APPID'),
    secret=os.environ.get('WEBOX_APPSECRET'),
    session=__session_interface
)

