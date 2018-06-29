# -*- coding: utf-8 -*-

import re
import requests
import datetime
from app.models import InternshipNews

KEYWORDS = ['校招', '秋招', '内推', '实习', 'intern']

HOST_URL = 'http://bbs.nju.edu.cn/'

SRC_URL = 'http://bbs.nju.edu.cn/bbsdoc?board=D_Computer'

PATTERN = '<tr><td>(\d+)<td>\s+<td><a[^>]*>\w+<\/a><td><td><nobr>([^<]*)<td><a href=([^>]*)>([^<]*)</a>'

YEAR_PATTERN = '发信站: 南京大学小百合站 \(([^)]+)\)'

SOURCE = '小百合'


def fetch_njubbs_computer():
    resp = requests.get(SRC_URL)
    if not resp:
        return
    html = resp.text
    item_pat = re.compile(PATTERN)
    items = item_pat.findall(html)

    keywords_pattern = '|'.join(KEYWORDS)
    exclude_pattern = 'Re:'

    for item in items:
        try:
            title = item[3].strip()
            if re.findall(exclude_pattern, title) or not re.findall(keywords_pattern, title):
                continue
            origin_id = item[0]
            url = HOST_URL + item[2]
            publish_time = _retrieve_year(url)
            news = InternshipNews(origin_id=origin_id, title=title, url=url, publish_time=publish_time, source=SOURCE)
            InternshipNews.add(news)
        except:
            continue


def _retrieve_year(url):
    html = requests.get(url).text
    items = re.findall(YEAR_PATTERN, html)
    if items:
        t = items[0]
        try:
            publish_time = datetime.datetime.strptime(t, '%a %b %d %H:%M:%S %Y')
            return publish_time
        except:
            return None
    return None


if __name__ == '__main__':
    fetch_njubbs_computer()
