# -*- coding: utf-8 -*-

import os
from configparser import ConfigParser

extra_config = ConfigParser()
extra_config.read(os.path.dirname(os.path.abspath(__file__))+ '/extra_config.ini')


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = extra_config['sqlalchemy']['dev_uri']
    FLASKY_MAIL_SUBJECT_PREFIX = '[internship_fetcher]'
    FLASKY_MAIL_SENDER = 'Hiki <aneureka2@gmail.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    # wechat
    TOKEN = extra_config['wechat']['token']
    APPID = extra_config['wechat']['appid']
    APP_SECRET = extra_config['wechat']['appsecret']
    ACCESS_TOKEN_KEY = extra_config['wechat']['access_token_key']
    BBS_MSG_TEMPLATE = 'VJjZl1Oxc6aQO-tL0YrlIRjbnenLGyuaFikBLw0Q1BA'
    TEST_OPENID = 'oizzE0QiwZj8jGTp9NzVKE2OR5Qc'


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
    SQLALCHEMY_DATABASE_URI = extra_config['sqlalchemy']['dev_uri']


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = extra_config['sqlalchemy']['test_uri']


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = extra_config['sqlalchemy']['prod_uri']


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
