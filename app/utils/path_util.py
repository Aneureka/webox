import os

__app_dir = os.path.dirname(os.path.abspath(__file__))
__base_dir = os.path.abspath(os.path.join(__app_dir, "../../"))


def base_dir():
    return __base_dir