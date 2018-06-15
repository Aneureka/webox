# -*- coding: utf-8 -*-
"""
微信公众平台 —— 信息验证
"""

import hashlib
from flask import current_app


def verify(data):
    if len(data) < 4:
        return "老哥，这个请求绝对不是微信的吧..."
    signature = data.get('signature')
    timestamp = data.get('timestamp')
    nonce = data.get('nonce')
    echostr = data.get('echostr')
    token = current_app.config['TOKEN']
    arr = [token, timestamp, nonce]
    arr.sort()
    hashcode = hashlib.sha1(''.join(arr).encode('utf-8')).hexdigest()
    if hashcode == signature:
        return echostr
    else:
        return "验证错误了嘤嘤嘤"


