# -*- coding: utf-8 -*-
"""
微信公众平台 —— 用户管理
"""

import requests
import json
import time
from app.wechat.access_token_helper import get_access_token
from app.models import User


def get_user_openids(next_openid=None):
    access_token = get_access_token()
    print(access_token)
    url = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token={ACCESS_TOKEN}' . format(ACCESS_TOKEN=access_token)
    if next_openid:
        url += '&next_openid={NEXT_OPENID}' . format(NEXT_OPENID=next_openid)
    data = json.loads(requests.get(url).content.decode('utf-8'))
    if data:
        if data.__contains__('errcode'):
            errcode = data['errcode']
            if errcode == -1:
                time.sleep(2)
                return get_user_openids(next_openid)
            else:
                print('获取Access token错误！')
        else:
            openids = []
            if 'data' in data.keys():
                openids = data['data']['openid']
            next_id = data['next_openid']
            if next_id:
                openids.extend(get_user_openids(next_id))
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
    access_token = get_access_token()
    url = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token={ACCESS_TOKEN}&openid={OPENID}&lang=zh_CN' . format(ACCESS_TOKEN=access_token, OPENID=openid)
    data = json.loads(requests.get(url).content.decode('utf-8'))
    print(data)
    if data:
        if data.__contains__('errcode'):
            errcode = data['errcode']
            if errcode == -1:
                time.sleep(2)
                return _get_user_info(openid)
            else:
                print('获取Access token错误！')
        else:
            return User(**data)
