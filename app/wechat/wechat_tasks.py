# -*- coding: utf-8 -*-

import sys
from app.utils.path_util import base_dir
sys.path.append(base_dir())

from app.utils.log_util import get_logger
from app.utils.conf_util import get_value
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
        if get_value('app', 'mode') == 'test':
            send_for_test()
        else:
            send_to_all()


if __name__ == '__main__':
    run_tasks()
