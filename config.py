# -*- coding: utf-8 -*-

import os
from configparser import ConfigParser

sensitive_config = ConfigParser()
print(os.path.dirname(os.path.abspath(__file__))+ '/sensitiveconfig.ini')
sensitive_config.read(os.path.dirname(os.path.abspath(__file__))+ '/sensitiveconfig.ini')


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = sensitive_config['sqlalchemy']['dev_uri']
    FLASKY_MAIL_SUBJECT_PREFIX = '[internship_fetcher]'
    FLASKY_MAIL_SENDER = 'Hiki <aneureka2@gmail.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    # 各网站配置
    V2EX_KEYWORDS = ['校招', '秋招', '内推', '2018', '2019', '2020', '实习']

    # 微信相关配置
    TOKEN = sensitive_config['wechat']['token']
    APPID = sensitive_config['wechat']['appid']
    APP_SECRET = sensitive_config['wechat']['appsecret']
    ACCESS_TOKEN_KEY = sensitive_config['wechat']['access_token_key']
    BBS_MSG_TEMPLATE = 'VJjZl1Oxc6aQO-tL0YrlIRjbnenLGyuaFikBLw0Q1BA'

    TEXT_MSG_TEMPLATE = """ 
                            <xml>
                            <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                            <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                            <CreateTime>{CreateTime}</CreateTime>
                            <MsgType><![CDATA[text]]></MsgType>
                            <Content><![CDATA[{Content}]]></Content>
                            </xml>
                            """
    IMAGE_MSG_TEMPLATE = """ 
                             <xml>
                             <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                             <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                             <CreateTime>{CreateTime}</CreateTime>
                             <MsgType><![CDATA[text]]></MsgType>
                             <Content><![CDATA[{Content}]]></Content>
                             </xml>
                             """

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = sensitive_config['sqlalchemy']['dev_uri'] or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = sensitive_config['sqlalchemy']['test_uri'] or 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = sensitive_config['sqlalchemy']['prod_uri'] or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
