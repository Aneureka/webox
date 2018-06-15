# -*- coding: utf-8 -*-

from . import api
from app import db


@api.route('/', methods=['GET'])
def index():
    return '连接成功~'

