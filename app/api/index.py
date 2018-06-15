# -*- coding: utf-8 -*-

from . import api
from app import db


@api.route('/', methods=['GET'])
def index():
    return '已经连接到服务器啦~'


@api.route('/api')
def show_api():
    html = """
           <h2>internship_fetcher api list</h2>
           <h3>V2EX</h3>
           <ul>
           <li>/api/v2ex</li>
           <li>/api/v2ex/today</li>
           <li>/api/v2ex/yesterday</li>
           </ul>
           """
    return html

