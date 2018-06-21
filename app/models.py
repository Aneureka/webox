# -*- coding: utf-8 -*-

from flask import jsonify
import datetime
from . import db


class InternshipNews(db.Model):
    __tablename__ = 'internship_news'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    source = db.Column(db.String(256), default='other')
    origin_id = db.Column(db.String(128), default='')
    title = db.Column(db.String(256), default='')
    url = db.Column(db.String(512), nullable=False)
    fetch_time = db.Column(db.DateTime, default=datetime.datetime.now())
    publish_time = db.Column(db.DateTime, nullable=True)
    company = db.Column(db.String(128), default='')
    address = db.Column(db.String(128), default='')

    @classmethod
    def add(cls, news):
        existed_news = cls.query.filter(cls.source == news.source).filter(cls.origin_id == news.origin_id).all()
        if len(existed_news) > 0:
            return
        try:
            db.session.add(news)
            db.session.commit()
        except:
            print('failed...')
            db.session.rollback()

    @classmethod
    def get_today(cls):
        today = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_news = cls.query.filter(cls.fetch_time >= today).limit(7).all()
        return today_news

    @classmethod
    def get_ystd(cls):
        today = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        yesterday = today - datetime.timedelta(days=1)
        ystd_news = cls.query.filter(cls.fetch_time >= yesterday).filter(cls.fetch_time < today).limit(7).all()
        return ystd_news

    @classmethod
    def get_latest(cls, n=7):
        latest_news = cls.query.order_by(cls.fetch_time.desc()).limit(n).all()
        return latest_news

    @classmethod
    def get_by_address(cls, address):
        news = cls.query.filter(cls.address.like('%'+address+'%')).order_by(cls.publish_time.desc()).limit(7).all()
        return news

    @classmethod
    def get_by_company(cls, company):
        news = cls.query.filter(cls.company.like('%'+company+'%')).order_by(cls.publish_time.desc()).limit(7).all()
        return news

    @classmethod
    def get_all(cls):
        all_news = cls.query.all()
        return all_news

    @classmethod
    def to_text(cls, news_list):
        if not news_list:
            return '暂时还没有消息呢，等会儿吧~'
        text = '--------------------------\n'.join([news.to_text_single() for news in news_list])
        return text

    def to_text_single(self):
        text = ''
        if self.source == 'v2ex':
            text = """【{source}】{title}\n{url}\n""".format(source=self.source, title=self.title, url=self.url)
        elif self.source == '牛客网':
            text = """【{source}】{title}\n※{address}※  {publish_time}\n{url}\n""".format(source=self.source, title=self.title, url=self.url, address=self.address, publish_time=self.publish_time.date())
        return text

    def to_dict(self):
        dict_data = {
            'id': self.id,
            'source': self.source,
            'origin_id': self.origin_id,
            'title': self.title,
            'url': self.url,
            'fetch_time': self.fetch_time,
            'publish_time': self.publish_time,
            'company': self.company,
            'address': self.address
        }
        return dict_data


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    source = db.Column(db.String(128), nullable=False)
    content = db.Column(db.String(512), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())

    @classmethod
    def add(cls, feedback):
        try:
            db.session.add(feedback)
            db.session.commit()
        except:
            db.session.rollback()

