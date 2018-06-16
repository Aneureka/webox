# -*- coding: utf-8 -*-

import json
from datetime import datetime, date


class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def to_json(src, cls=DatetimeEncoder):
    return json.dumps(src, cls=cls)




