# -*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
import jieba
from app.utils.log_util import get_logger
from app.models import InternshipNews
from app.utils.time_util import get_datetime_from_timestamp

ADDRESSES = ['北京', '上海', '杭州', '成都', '深圳', '西安', '苏州', '广州', '南京', '青岛', '大连', '武汉', '留学生']

# COMPANIES = {'百度', '阿里', '腾讯', '京东', '亚马逊', 'Google', '网易', '美团', '头条', '滴滴', '新浪', '搜狐', '携程', '小米', '苏宁', '字节跳动', '拼多多', '高盛', '摩根士丹利', '下厨房', '微软', '华为'}

LIST_URL_TEMPLATE = 'https://www.nowcoder.com/recommend-intern/list?page={PAGE}&address={ADDRESS}'
DETAIL_URL_TEMPLATE = 'https://www.nowcoder.com/recommend-intern/{INTERN_COMPANY_ID}?jobId={JOB_ID}'


def fetch_nowcoder():
    for address in ADDRESSES:
        page = 1
        while True:
            list_url = LIST_URL_TEMPLATE.format(ADDRESS=address, PAGE=page)
            json_data = requests.get(list_url).json()
            if not json_data:
                break
            job_list = [] if not json_data.get('data') else json_data.get('data').get('jobList')
            if not job_list:
                break
            for job in job_list:
                try:
                    store_job_news(job)
                except:
                    get_logger().warning('fetch job detail info failed at job ' + str(job.get('id')))
                    continue
            page += 1


def store_job_news(job):
    source = '牛客网'
    origin_id = job.get('id')
    title = job.get('title')
    url = DETAIL_URL_TEMPLATE.format(INTERN_COMPANY_ID=job.get('internCompanyId'), JOB_ID=origin_id)
    publish_time = get_datetime_from_timestamp(job.get('createTime'))
    company = retrieve_company_name(url)
    address = job.get('address')
    news = InternshipNews(source=source, origin_id=origin_id, title=title, url=url, publish_time=publish_time, company=company, address=address)
    InternshipNews.add(news)


def retrieve_company_name(job_url):
    resp = requests.get(job_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    company = soup.find('h3', class_='teacher-name').get_text()
    return company


if __name__ == '__main__':
    fetch_nowcoder()
