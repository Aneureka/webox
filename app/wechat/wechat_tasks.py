# -*- coding: utf-8 -*-

import sys
import os
app_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.abspath(os.path.join(app_dir, "../"))
sys.path.append(base_dir)

from app.utils.log_util import get_logger
from wechatpy.exceptions import APILimitedException

from manage import app
from app.wechat.wechat_user import get_user_openids, update_users
from app.wechat.wechat_message import send_to_all, send_for_test


def run_tasks():
    with app.app_context():
        try:
            update_users(get_user_openids())
        except APILimitedException:
            get_logger().warning('get followers api limited')
        if os.environ.get('MODE') == 'all':
            send_to_all()
        else:
            send_for_test()


if __name__ == '__main__':
    run_tasks()
