# -*- coding: utf-8 -*-

import os
import sys

app_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.abspath(os.path.join(app_dir, "../"))
sys.path.append(base_dir)

from manage import app
from app.spiders.v2ex_spider import fetch_v2ex


def run_tasks():
    with app.app_context():
        fetch_v2ex()


if __name__ == '__main__':
    run_tasks()
