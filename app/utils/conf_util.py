# -*- coding: utf-8 -*-

from configparser import ConfigParser
from app.utils.path_util import base_dir

__config = ConfigParser()
__config_path = base_dir() + '/extra_config.ini'

__config.read(__config_path, encoding='utf-8')


def get_value(section, key):
    return __get_value(section, key)


def __get_value(section, key, chances=1):
    if section in __config and key in __config[section]:
        return __config[section][key]
    else:
        if chances > 0:
            __config.read(__config_path)
            __get_value(section, key, chances-1)
        else:
            return None


if __name__ == '__main__':
    print(get_value('wechat', 'token'))