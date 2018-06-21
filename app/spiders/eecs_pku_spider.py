# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


def fetch_eecs_pku():
    src_url = 'http://eecs.pku.edu.cn/personnel/YJS/RecruitStudents/'
    resp = requests.get(src_url)
    # print(resp.text)
    soup = BeautifulSoup(resp.text, 'html.parser')

    container = soup.find('ul', class_='xyxwM2 not_ann')
    items = container.findAll('li')

    res = []

    for item in items:
        url = src_url + item.find('a').get('href')
        title = item.find('h1', class_='xyxwM2Rh1').string
        res.append(title + '\n' + url)

    return '\n---------------\n'.join(res[:5])


if __name__ == '__main__':
    print(fetch_eecs_pku())