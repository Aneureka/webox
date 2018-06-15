# -*- coding: utf-8 -*-

import os
import sys

app_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.abspath(os.path.join(app_dir, "../../"))
sys.path.append(base_dir)

from manage import app
from app.wechat.user_manager import get_user_openids, update_users
from app.wechat.message_sender import send_to_all


def run_tasks():
    with app.app_context():
        update_users(get_user_openids())
        send_to_all()


if __name__ == '__main__':
    run_tasks()
