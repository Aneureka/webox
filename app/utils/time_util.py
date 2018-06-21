# -*- coding: utf-8 -*-

import datetime


def get_cur_timestamp():
    return int(datetime.datetime.now().timestamp())


def get_datetime_from_timestamp(milli_sec_stamp):
    return datetime.datetime.fromtimestamp(milli_sec_stamp / 1000)


if __name__ == '__main__':
    print(get_datetime_from_timestamp(1478830547000))