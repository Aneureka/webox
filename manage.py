# -*- coding: utf-8 -*-

import os
import logging
from app import create_app
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


def make_shell_context():
    return dict(app=app)


def setup_logging():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p')




manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()