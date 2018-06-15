# -*- coding: utf-8 -*-

from . import api
from app.utils.json_util import to_json
from app.models import V2EXNews


@api.route('/api/v2ex')
def get_all_news():
    """获取所有的v2ex实习信息"""
    return to_json(V2EXNews.get_all())


@api.route('/api/v2ex/today')
def get_today_news():
    """获取今天的v2ex实习信息"""
    return to_json(V2EXNews.get_today())


@api.route('/api/v2ex/yesterday')
def get_ystd_news():
    return to_json(V2EXNews.get_ystd())



