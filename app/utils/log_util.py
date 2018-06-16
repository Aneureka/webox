import logging
import datetime
from app.utils.path_util import base_dir


def get_logger(name=None):
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(filename)s %(lineno)d -- %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    # setup handler
    handler = logging.FileHandler(base_dir() + '/logs/' + str(datetime.date.today()) + '.log')
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger





