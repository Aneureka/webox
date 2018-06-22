# -*- coding: utf-8 -*-

import os
from . import api
from flask import request, jsonify
from app.models import InternshipNews
from app.tasks import *
from app.utils.log_util import get_logger


@api.route('/api/news')
def get_all_news():
    return jsonify(news=[news.to_dict() for news in InternshipNews.get_all()])


@api.route('/api/news/today')
def get_today_news():
    return jsonify(news=[news.to_dict() for news in InternshipNews.get_today()])


@api.route('/api/news/yesterday')
def get_ystd_news():
    return jsonify(news=[news.to_dict() for news in InternshipNews.get_ystd()])


@api.route('/api/news/latest')
def get_latest_news():
    data = request.args.to_dict()
    n = data.get('n')
    if n:
        return jsonify(news=[news.to_dict() for news in InternshipNews.get_latest(int(n))])
    else:
        return jsonify(news=[news.to_dict() for news in InternshipNews.get_latest()])


@api.route('/api/news/fetch')
def fetch():
    data = request.args.to_dict()
    token = data.get('token')
    if not token or token != os.environ.get('WEBOX_AUTHORIZATION_KEY'):
        return 'You are not authorized to view the access token!'
    else:
        source = data.get('source')
        spider_tasks = {
            'v2ex': run_spider_v2ex,
            'nowcoder': run_spider_nowcoder,
            'njubbs': run_spider_njubbs
        }

        if source:
            spider_tasks[source]()
            get_logger().info('fetch {source} internship news'.format(source=source))
        else:
            run_spider_news()
            get_logger().info('fetch all internship news')
        return 'fetched successfully!'
