# -*- coding: utf-8 -*-
"""
时间工具
"""

from datetime import datetime


def get_cur_timestamp():
    return int(datetime.now().timestamp())

