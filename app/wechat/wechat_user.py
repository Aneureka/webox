# -*- coding: utf-8 -*-

import json
from app.models import User
from app.wechat.wechat_sdk import wechat_client
from wechatpy.client.api import WeChatUser
from app.utils.log_util import get_logger

_wechat_user = WeChatUser(wechat_client)


def get_user_openids(next_openid=None):
    data = _wechat_user.get_followers(None)
    logger = get_logger()
    openids = []
    if data:
        if data.__contains__('errcode'):
            logger.warning('unable to get followers')
            return openids
        else:
            if 'data' in data.keys():
                openids = data['data']['openid']
            return openids


def update_users(openids):
    for openid in openids:
        if User.exists(openid):
            continue
        else:
            try:
                user = _get_user_info(openid)
                User.add(user)
            except:
                continue


def _get_user_info(openid):
    user = json.loads(_wechat_user.get(openid))
    logger = get_logger()
    if user:
        if user.__contains__('errcode'):
            logger.warning('unable to get user info')
        else:
            return User(**user)
