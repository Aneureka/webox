# -*- coding: utf-8 -*-

from app.spiders.v2ex_spider import fetch_v2ex
from app.spiders.nowcoder_spider import fetch_nowcoder


def fetch_news():
    fetch_v2ex()
    fetch_nowcoder()