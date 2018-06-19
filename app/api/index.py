# -*- coding: utf-8 -*-

from . import api


@api.route('/', methods=['GET'])
def index():
    return '已经连接到服务器啦~'


@api.route('/api')
def show_api():
    html = '<h2>就先不展示了哈</h2>'
    return html

