# -*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
from app.models import InternshipNews

KEYWORDS = ['校招', '秋招', '内推', '2018', '2019', '2020', '实习']

SRC_URL = 'https://www.v2ex.com/?tab=jobs'


def fetch_v2ex():
    resp = requests.get(SRC_URL)
    soup = BeautifulSoup(resp.text, 'html.parser')

    items = soup.find_all('span', class_='item_title')
    keywords_pattern = '|'.join(KEYWORDS)

    for item in items:
        title = item.get_text()
        short_url = item.find('a').get('href')
        id = str(short_url.split('/')[-1].split('#')[0])
        url = 'https://www.v2ex.com/t/' + id

        pat = re.findall(keywords_pattern, title)
        if not pat:
            continue
        InternshipNews.add(InternshipNews(source='v2ex', origin_id=id, title=title, url=url))

