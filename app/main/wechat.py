# -*- coding: utf-8 -*-

from . import main
from flask import request, current_app
from app.wechat.verify import verify
from app.wechat.access_token_helper import get_access_token


@main.route('/wechat', methods=['GET', 'POST'])
def wechat_core():
    """微信核心交互接口"""
    if request.method == 'GET':
        # 验证token
        data = request.args.to_dict()
        return verify(data)
    else:
        # todo 处理信息
        return '人家还不用实现这个啦..'


@main.route('/wechat/access_token', methods=['GET'])
def access_token():
    """获取Access token"""
    data = request.args.to_dict()
    key = data.get('key')
    if not key or key != current_app.config['ACCESS_TOKEN_KEY']:
        return '老哥，还想来偷看我的密钥，我已经记住你IP了。'
    return get_access_token()


