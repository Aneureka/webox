# -*- coding: utf-8 -*-

from . import api
from app.models import V2EXNews
from app.spiders.v2ex_spider import fetch_v2ex
from flask import render_template, session, redirect, url_for, request, current_app


@api.route('/v2ex/today')
def get_today_news():
    """获取今天的v2ex实习信息"""
    return V2EXNews.get_today()


@api.route('/v2ex')
def get_all_news():
    """获取所有的v2ex实习信息"""
    return V2EXNews.get_all()


@api.route('/v2ex/yesterday')
def get_ystd_news():
    return V2EXNews.get_ystd()


@api.route('/v2ex/add')
def test_add():
    """测试添加记录"""
    fetch_v2ex()
    return '测试加入完成~'