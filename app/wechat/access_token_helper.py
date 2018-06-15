# -*- coding: utf-8 -*-
"""
微信公众平台 —— 管理Access_token
"""
# -*- coding: utf-8 -*-

import requests
import json
import time
from flask import current_app

from app.utils.time_util import get_cur_timestamp
from app.utils.redis_helper import get_redis

_redis = get_redis()


def get_access_token():
    access_token = _redis.get('access_token')
    expired_time = -1 if _redis.get('expired_time') is None else int(_redis.get('expired_time'))
    if not access_token or expired_time < get_cur_timestamp():
        _update_access_token()
    return _redis.get('access_token')


def _update_access_token():
    # 获取Access Token
    appid = current_app.config['APPID']
    appsecret = current_app.config['APP_SECRET']
    at_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}'.format(
        APPID=appid, APPSECRET=appsecret)
    data = json.loads(requests.get(at_url).content.decode('utf-8'))
    if data:
        if data.__contains__('errcode'):
            errcode = data['errcode']
            if errcode == -1:
                time.sleep(2)
                _update_access_token()
            elif errcode == 40164:
                print(data['errmsg'])
            else:
                print('获取Access token错误！')
        else:
            access_token = data['access_token']
            expires_in = int(data['expires_in']/2)
            expired_time = get_cur_timestamp() + expires_in
            _redis.set('access_token', access_token)
            _redis.set('expired_time', expired_time)

