# -*- coding: utf-8 -*-

from app.spiders.v2ex_spider import fetch_v2ex
from app.spiders.nowcoder_spider import fetch_nowcoder
from app.spiders.njubbs_spider import fetch_njubbs_computer


def run_spider_news():
    run_spider_v2ex()
    run_spider_nowcoder()
    run_spider_njubbs()


def run_spider_v2ex():
    fetch_v2ex()


def run_spider_nowcoder():
    fetch_nowcoder()


def run_spider_njubbs():
    fetch_njubbs_computer()