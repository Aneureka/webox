# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, date, time
import json
# from bson import json_util
from . import db


class V2EXNews(db.Model):
    __tablename__ = 'v2ex_news'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    fetch_time = db.Column(db.DateTime, default=datetime.now())

    @classmethod
    def add(cls, id, url, title):
        news = cls(id=id, url=url, title=title)
        try:
            db.session.add(news)
            db.session.commit()
        except:
            db.session.rollback()

    @classmethod
    def get_today(cls):
        today = datetime.combine(date.today(), time.min)
        today_news_list = cls.query.filter(cls.fetch_time >= today).all()
        dict_news = {'news': [news.to_dict() for news in today_news_list]}
        return json.dumps(dict_news, cls=DatetimeEncoder)

    @classmethod
    def get_ystd(cls):
        today = datetime.combine(date.today(), time.min)
        yesterday = today - timedelta(days=1)
        ystd_news_list = cls.query \
            .filter(cls.fetch_time >= yesterday) \
            .filter(cls.fetch_time < today) \
            .order_by(cls.fetch_time.desc()) \
            .all()
        dict_news = {'news': [news.to_dict() for news in ystd_news_list]}
        return json.dumps(dict_news, cls=DatetimeEncoder)

    @classmethod
    def get_all(cls):
        news_list = cls.query.all()
        dict_news = {'news': [news.to_dict() for news in news_list]}
        return json.dumps(dict_news, cls=DatetimeEncoder)

    def to_dict(self):
        dict_news = {
            'title': self.title,
            'url': self.url,
            'fetch_time': self.fetch_time
        }
        return dict_news


class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
