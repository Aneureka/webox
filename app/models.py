# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, date, time
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
        return dict_news

    @classmethod
    def get_ystd(cls):
        today = datetime.combine(date.today(), time.min)
        yesterday = today - timedelta(days=1)
        ystd_news_list = cls.query \
            .filter(cls.fetch_time >= yesterday) \
            .filter(cls.fetch_time < today) \
            .order_by(cls.fetch_time) \
            .all()
        dict_news = {'news': [news.to_dict() for news in ystd_news_list]}
        return dict_news

    @classmethod
    def get_all(cls):
        news_list = cls.query.all()
        dict_news = {'news': [news.to_dict() for news in news_list]}
        return dict_news

    def to_dict(self):
        dict_news = {
            'title': self.title,
            'url': self.url,
            'fetch_time': self.fetch_time
        }
        return dict_news


class User(db.Model):
    __tablename__ = 'user'
    openid = db.Column(db.String(100), primary_key=True)
    nickname = db.Column(db.String(50), default='')
    sex = db.Column(db.Integer, default=0)
    country = db.Column(db.String(50), default='')
    province = db.Column(db.String(50), default='')
    city = db.Column(db.String(50), default='')
    headimgurl = db.Column(db.String(200), default='')
    subscribe_time = db.Column(db.Integer, default=0)

    def __init__(self, *args, **kwargs):
        for dictionary in args:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

    @classmethod
    def add_from_openid(cls, openid):
        user = cls(openid=openid)
        try:
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()

    @classmethod
    def add(cls, user):
        try:
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()

    @classmethod
    def get_all_openid(cls):
        user_list = cls.query.all()
        openid_list = [user.openid for user in user_list]
        return openid_list

    @classmethod
    def exists(cls, openid):
        records = cls.query.filter(cls.openid == openid).all()
        return True if records else False

