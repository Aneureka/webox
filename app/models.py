# -*- coding: utf-8 -*-

from flask import jsonify
import datetime
from . import db


class InternshipNews(db.Model):
    __tablename__ = 'internship_news'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    source = db.Column(db.String(256), default='other')
    origin_id = db.Column(db.String(128), default='')
    title = db.Column(db.String(256), nullable=False)
    url = db.Column(db.String(512), nullable=False)
    fetch_time = db.Column(db.DateTime, default=datetime.datetime.now())
    other_info = db.Column(db.String(256), default='')

    @classmethod
    def add(cls, news):
        existed_news = cls.query.filter(cls.source == news.source).filter(cls.origin_id == news.origin_id).all()
        if len(existed_news) > 0:
            return
        try:
            db.session.add(news)
            db.session.commit()
        except:
            db.session.rollback()

    @classmethod
    def get_today(cls):
        today = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_news = cls.query.filter(cls.fetch_time >= today).all()
        return cls.to_text(today_news)

    @classmethod
    def get_ystd(cls):
        today = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        yesterday = today - datetime.timedelta(days=1)
        ystd_news = cls.query.filter(cls.fetch_time >= yesterday).filter(cls.fetch_time < today).all()
        return cls.to_text(ystd_news)

    @classmethod
    def get_latest(cls, n=7):
        latest_news = cls.query.order_by(cls.fetch_time.desc()).limit(n).all()
        return cls.to_text(latest_news)

    @classmethod
    def get_all(cls):
        all_news = cls.query.all()
        return cls.to_text(all_news)

    @classmethod
    def to_text(cls, news_list):
        if not news_list:
            return '暂时还没有消息呢，等会儿吧~'
        text = '--------------------------\n' . join([news.to_text_single() for news in news_list])
        return text

    def to_text_single(self):
        text = """【{source}】{title}\n{url}\n""" . format(source=self.source, title=self.title, url=self.url)
        return text

    def to_dict(self):
        dict_data = {
            'id': self.id,
            'source': self.source,
            'origin_id': self.origin_id,
            'title': self.title,
            'url': self.url,
            'fetch_time': self.fetch_time,
            'other_info': self.other_info
        }
        return dict_data



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

